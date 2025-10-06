import logging
import re
import time
from collections.abc import Iterable
from operator import itemgetter
from typing import TypedDict, Union

from .utils import _make_get_request, _make_post_request, general_headers, map_in_thread

_URL_API = 'https://api.contest.yandex.net/api/public/v2'
_CONTEST_URL = _URL_API + '/contests/{contest_id}'
_SUBMISSION_URL = _CONTEST_URL + '/submissions'
_SUBMISSION_INFO_URL = _SUBMISSION_URL + '/{run_id}'
_PROBLEM_URL = _CONTEST_URL + '/problems'
_STATEMENT_URL = _PROBLEM_URL + '/{alias}/statement'

_logger = logging.getLogger(__name__)

NOT_READY_STR = 'No report'
OK = 'OK'


class ProblemInfo(TypedDict):
    available_compilers: list[str]
    compiler: str


class BadTokenException(Exception):
    pass


# mypy: disable-error-code="index, union-attr, arg-type, return-value"
def get_contest_problems(token: str, contest_id: int) -> list[dict[str, ProblemInfo]]:
    url = _PROBLEM_URL.format(contest_id=contest_id)
    headers = general_headers(token)
    resp, status = _make_get_request(url, headers)
    if status != 200:
        if status == 401:
            raise BadTokenException('Invalid or missed token')
        raise NotImplementedError(f'Can\'t make request "{url}". Got {resp["error"]}')  # type: ignore[index]
    try:
        _logger.info('Got %d problems', len(resp['problems']))  # type: ignore[index]
        problems = []
        p = re.compile(r'(pypy|python)')
        for problem in sorted(resp['problems'], key=itemgetter('alias')):  # type: ignore[index]
            alias: str = problem['alias']
            _logger.debug('For task %s got compilers: %s', alias, ', '.join(problem['compilers']))
            task = ProblemInfo(
                available_compilers=list(filter(p.search, problem['compilers'])),
                compiler=''
            )
            if len(task['available_compilers']) > 0:
                task['compiler'] = task['available_compilers'][0]
            else:
                raise Exception(f'No known compilers in problem {alias}')
            problems.append({alias: ProblemInfo(**task)})
            _logger.info('Set default compiler "%s" for problem %s.',
                         task['compiler'], alias)
    except Exception as e:
        raise NotImplementedError(f'Can\'t parse responce from "{url}". Got {e}')
    return problems


_pio = re.compile(
    r'<table class="sample-tests">.*?<th>Ввод</th>.*?<th>Вывод</th>.*?<td><pre>(.*?)</pre></td>.*?<td><pre>(.*?)</pre></td>.*?</table>', re.DOTALL)


def _extract_from_text(s: str) -> list[tuple[str, str]]:
    return _pio.findall(s)


def get_problem_input_output(token: str, contest_id: int, problem: str, prompt_in: str, prompt_out: str) -> tuple[str, str, str]:
    url = _STATEMENT_URL.format(contest_id=contest_id, alias=problem)
    headers = general_headers(token, 'application/octet-stream')
    resp, status = _make_get_request(url, headers, False)
    if status != 200:
        if status == 401:
            raise BadTokenException('Invalid or missed token')
        raise NotImplementedError(f'Can\'t make request "{url}". Got {resp["error"]}')  # type: ignore[index]
    _logger.debug('Problem %s raw file must contain %d tests', problem, resp.count('Ввод'))  # type: ignore[union-attr]
    raw_input_output = _extract_from_text(resp)  # type: ignore[arg-type]
    input_output = []
    prompt_in += '\n'
    prompt_out += '\n'
    for inp, out in raw_input_output:
        if not inp.endswith('\n'):
            inp += '\n'
        if not out.endswith('\n'):
            out += '\n'
        input_output.append(prompt_in + inp + prompt_out + out)
    _logger.debug('Got %d tests for task %s', len(input_output), problem)
    return (problem, resp, ''.join(input_output))  # type: ignore[return-value]


def get_problems_io(token: str, contest_id: int, problems: Iterable[str], prompt_in: str, prompt_out: str) -> list[tuple[str, str, str]]:
    params = ((token, contest_id, p, prompt_in, prompt_out) for p in problems)
    result = map_in_thread(get_problem_input_output, params)
    return result


def send_solution(contest_id: int, problem: str, text: str, compiler: str, token: str) -> int:
    # 'https://api.contest.yandex.net/api/public/v2/contests/53029/submissions'
    url = _SUBMISSION_URL.format(contest_id=contest_id)
    # Граница для multipart
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    # Формируем тело запроса
    body = (
        f'--{boundary}\r\n'
        'Content-Disposition: form-data; name="compiler"\r\n\r\n'
        f'{compiler}\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{problem}.py"\r\n'
        'Content-Type: text/x-python\r\n\r\n'
        f'{text}'
        f'\r\n--{boundary}\r\n'
        'Content-Disposition: form-data; name="problem"\r\n\r\n'
        f'{problem}\r\n'
        f'--{boundary}--\r\n'
    ).encode()
    headers = {
        **general_headers(token),
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(body))
    }
    resp, status = _make_post_request(url, body, headers, False)
    if status != 200:
        raise Exception(f'Can\'t send. Error: {resp["error"]}')
    _logger.info('The solution %s has been send', problem)
    return resp['runId']


# mypy: disable-error-code="index, union-attr, arg-type, return-value"
def get_submission_result(contest_id: int, run_id: int, token: str) -> tuple[str, int]:
    url = _SUBMISSION_INFO_URL.format(contest_id=contest_id, run_id=run_id)
    headers = general_headers(token)
    resp, status = _make_get_request(url, headers)
    if status != 200:
        raise Exception(f'Can\'t get result, got: {resp["error"]}')  # type: ignore[index]
    verdict = resp['verdict']  # type: ignore[index]
    if verdict == NOT_READY_STR:
        short_verdict = verdict
    else:
        short_verdict = ''.join(filter(str.isupper, verdict))
    testnum = resp['testNumber']  # type: ignore[index]
    return short_verdict, testnum  # type: ignore[return-value]


def wait_submission_result(contest_id: int, run_id: int, token: str, seconds: int) -> tuple[str, Union[int, None]]:
    sleep_seconds = max(seconds // 10, 1)  # минимум секунду ждем
    start = time.perf_counter()
    verdict, testnum = NOT_READY_STR, None
    while time.perf_counter() - start <= seconds:
        verdict, testnum = get_submission_result(contest_id, run_id, token)
        if verdict != NOT_READY_STR:
            break
        _logger.info('The result is not ready yet. Waiting for %d seconds.', sleep_seconds)
        time.sleep(sleep_seconds)
    return verdict, testnum
