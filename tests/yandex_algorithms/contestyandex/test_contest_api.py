import json
from unittest.mock import Mock, patch

from yandex_algorithms.modules.contestyandex.contest_api import (
    ProblemInfo,
    _extract_from_text,
    get_contest_problems,
    get_problem_input_output,
    get_problems_io,
    get_submission_result,
    send_solution,
    wait_submission_result,
)

# from tests.yandex_algorithms.contestyandex import api_response
# from tests.yandex_algorithms.contestyandex.api_response import (
#     file_content,
#     submission_info,
# )
from .conftest import mock_constructor


def test_get_contest_problems_return_dict(urlopen_mock: Mock, token: str, contest_id: int, problems: dict):
    mock_constructor(urlopen_mock, 200, json.dumps(problems).encode('utf-8'))
    probems = get_contest_problems(token, contest_id)
    urlopen_mock.assert_called_once()
    assert isinstance(probems, list)
    assert len(probems) > 0
    for problem in probems:
        assert isinstance(problem, dict)
        assert len(list(problem.keys())) == 1
        assert list(problem.values())[0].keys(), ProblemInfo.__annotations__.keys()


def test_extract_from_text(file_content: str):
    input_output = _extract_from_text(file_content)
    assert len(input_output) == 3


def test_get_problem_input_output(urlopen_mock: Mock, token: str, contest_id: int, file_content: str):
    mock_constructor(urlopen_mock, 200, file_content.encode('utf-8'))
    prompt_in, prompt_out = '>', '<'
    problem, condition, inputs = get_problem_input_output(token, contest_id, 'A', prompt_in, prompt_out)
    urlopen_mock.assert_called_once()
    assert 'A' == problem
    for s in inputs.lstrip(prompt_in + '\n').split(prompt_in + '\n'):
        i, o = s.split(prompt_out + '\n')
        assert i in condition
        assert o in condition


@patch('yandex_algorithms.modules.contestyandex.contest_api.get_problem_input_output')
def test_get_problems_io(mock: Mock, token: str, contest_id: int):
    problems = ['A', 'C', 'D']
    mock.side_effect = [[x, '', ''] for x in problems]
    result = get_problems_io(token, contest_id, problems, '>', '<')
    for r in result:
        assert len(r) == 3
        assert r[0] in problems


def test_send_submission(urlopen_mock: Mock, token: str, contest_id: int):
    run_id = 1
    mock_constructor(urlopen_mock, 200, json.dumps({'runId': run_id}).encode('utf-8'))
    problem = 'A'
    text = "print('Hello, world!')\n"
    result = send_solution(contest_id, problem, text, 'pypy', token)
    assert run_id == result
    urlopen_mock.assert_called_once()
    req = urlopen_mock.call_args.args[0]
    assert req.headers['Content-type'].startswith('multipart/form-data; boundary=')
    assert text in req.data.decode('utf-8')


def test_get_submission_result(urlopen_mock: Mock, token: str, contest_id: int, submission_info: dict):
    run_id = 1
    mock_constructor(urlopen_mock, 200, json.dumps(submission_info).encode('utf-8'))
    verdict, testnum = get_submission_result(contest_id, run_id, token)
    assert 'OK' == verdict
    assert 0 == testnum


def test_wait_submission_result(urlopen_mock: Mock, token: str, contest_id: int, submission_info: dict):
    run_id = 1
    mock_constructor(urlopen_mock, 200, json.dumps(submission_info).encode('utf-8'))
    verdict, testnum = wait_submission_result(contest_id, run_id, token, 2)
    assert 'OK' == verdict
    assert 0 == testnum
