import logging
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Union

from .config import load_config, store_config
from .contest_api import (
    BadTokenException,
    ProblemInfo,
    get_contest_problems,
    get_problems_io,
    send_solution,
    wait_submission_result,
)
from .oauth_api import authenticate_yandex

_logger = logging.getLogger(__name__)


def init(url: str, **params):
    m = re.search(r'/contest/(?P<id_>\d+)', url)
    if m is None:
        raise NotImplementedError(f'Can\'t get contest id from {url}')
    contest_id = int(m.group('id_'))
    conf = load_config()
    token = params.get('token') or conf['token']
    try:
        _logger.debug('Try to get problems with token=%s', token)
        problems_info = get_contest_problems(token, contest_id)
    except BadTokenException:
        client_id = params.get('client_id')
        client_secret = params.get('client_secret')
        assert client_id is not None and client_secret is not None, \
            'Bad token. Need client_id and client_secret in params to get token'
        _logger.debug('Try to get problems with client_id=%s and client_secret=%s',
                      client_id, client_secret)
        token = authenticate_yandex(client_id, client_secret)
        problems_info = get_contest_problems(token, contest_id)
    store_config(token, contest_id, problems_info)


def load_problems(prompt_in: str, prompt_out: str,
                  problems: Union[Iterable[str], None] = None) -> list[tuple[str, str, str]]:
    conf = load_config()
    token = conf['token']
    contest_id = conf['contest_id']
    if problems is None:
        if len(conf['problems']) == 0:
            raise Exception('No problems found in config')
        problems = list(conf['problems'].keys())
    problems_io = get_problems_io(token, contest_id, problems, prompt_in, prompt_out)
    return problems_io


def send_submission(solution: str, wait_seconds: int) -> tuple[str, Union[int, None]]:
    conf = load_config()
    token = conf['token']
    contest_id = conf['contest_id']
    problem_info: Union[dict, ProblemInfo] = conf['problems'].get(solution, {})
    assert 'compiler' in problem_info, f'No compiler found in config for solution {solution}'
    compiler = problem_info['compiler']
    file = Path(f'{solution}.py')
    assert file.exists() and file.is_file(), f'Solution does\'t exists in path {file.absolute()}'
    text = file.read_text()
    run_id = send_solution(contest_id, solution, text, compiler, token)
    verdict, testnum = wait_submission_result(contest_id, run_id, token, wait_seconds)
    return verdict, testnum
