from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from yandex_algorithms.modules.contestyandex.commands import (
    init,
    load_problems,
    send_submission,
)
from yandex_algorithms.modules.contestyandex.config import _PROBLEM_PREFIX


@patch('yandex_algorithms.modules.contestyandex.commands.get_contest_problems')
def test_init_store_config(mock_gcp: Mock, token: str, contest_id: int, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    url = f'https://contest.yandex.ru/contest/{contest_id}/problems/A'
    params = {'token': token}
    mock_gcp.return_value = [{'A': {'available_compilers': [], 'compiler': ''}}]
    init(url, **params)
    conf_file = tmp_path / '.cfg'
    assert conf_file.exists()
    text = conf_file.read_text()
    assert token in text
    assert str(contest_id) in text
    assert f'{_PROBLEM_PREFIX}A' in text


@patch('yandex_algorithms.modules.contestyandex.contest_api.get_problem_input_output')
@patch('yandex_algorithms.modules.contestyandex.commands.load_config')
def test_load_problems(conf_mock: Mock, get_problem_mock: Mock,
                       token: str, contest_id: int):
    conf_mock.return_value = {'token': token, 'contest_id': contest_id}
    expected_problems = ('A', 'B', 'C')
    get_problem_mock.side_effect = [(x, '', '') for x in expected_problems]
    result = load_problems('>', '<', expected_problems)
    assert len(result) == len(expected_problems)
    for r in result:
        assert isinstance(r, tuple)
        assert len(r) == 3
        assert r[0] in expected_problems


@patch('yandex_algorithms.modules.contestyandex.commands.wait_submission_result')
@patch('yandex_algorithms.modules.contestyandex.commands.send_solution')
@patch('yandex_algorithms.modules.contestyandex.commands.load_config')
def test_send_submission(conf_mock: Mock, send_mock: Mock, wait_mock: Mock,
                         token: str, contest_id: int,
                         tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    solution, wait_seconds = 'A', 10
    compiler = 'pypy'
    conf_mock.return_value = {
        'token': token, 'contest_id': contest_id,
        'problems': {solution: {'compiler': compiler}}}
    text = 'print("Hello, world!")\n'
    run_id = 1
    expected_verdict, expected_testnum = 'RE', 1
    monkeypatch.chdir(tmp_path)
    (tmp_path / f'{solution}.py').write_text(text)
    send_mock.return_value = run_id
    wait_mock.return_value = (expected_verdict, expected_testnum)
    verdict, testnum = send_submission(solution, wait_seconds)  # type: ignore # должен быть результат
    assert expected_verdict == verdict
    assert expected_testnum == testnum
    send_mock.assert_called_once_with(contest_id, solution, text, compiler, token)
    wait_mock.assert_called_once_with(contest_id, run_id, token, wait_seconds)
