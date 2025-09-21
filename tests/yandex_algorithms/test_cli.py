from functools import reduce
from operator import add, itemgetter
from pathlib import Path
from typing import Union
from unittest.mock import Mock, patch

import pytest

from yandex_algorithms.cli import main


@pytest.fixture  # (autouse=True)
def cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    folder = tmp_path / 'tmp_folder'
    folder.mkdir()
    monkeypatch.chdir(folder)
    return folder

# _task_count = 3


def _split(s: str) -> Union[str, None]:
    return s.split()[-1] if s else None


@pytest.fixture(params=('-t 3', '--task-count 3',
                        '-u url', '--from-url url'), ids=('st', 'lt', 'su', 'lu'))
def task_count_or_url(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    if s.split()[1].isdigit():
        v = {'task_count': int(s.split()[1]), 'from_url': None}
    else:
        v = {'task_count': None, 'from_url': s.split()[1]}
    return s, v


@pytest.fixture(params=('', '-i inp', '--infilevar inp'), ids=('ei', 'si', 'li'))
def infilevar(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'infilevar': _split(s) or ''}
    return s, v


@pytest.fixture(params=('', '-o inp', '--outfilevar out'), ids=('eo', 'so', 'lo'))
def outfilevar(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'outfilevar': _split(s) or ''}
    return s, v


@pytest.fixture(params=('', "-m '>;<", "--prompts '>>>;<<<'"), ids=('em', 'sm', 'lm'))
def prompts(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'prompts': _split(s) or '-->;<--'}
    return s, v


@pytest.fixture(params=('', '-n', '--no-attempts-folder'), ids=('en', 'sn', 'ln'))
def no_attempts_folder(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'no_attempts_folder': bool(s)}
    return s, v


@pytest.fixture(params=('', '-p k1=v1 -p k2=v2', '--param k1=v1 --param k2=v2'), ids=('ep', 'sp', 'lp'))
def params(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'params': list(itemgetter(1, 3)(s.split())) if s else []}
    return s, v


@pytest.fixture
def init_str_with_kwargs(no_attempts_folder: tuple[str, dict], prompts: tuple[str, dict], outfilevar: tuple[str, dict],
                         infilevar: tuple[str, dict], task_count_or_url: tuple[str, dict], params: tuple[str, dict]) -> tuple[str, dict]:
    s = ' '.join((
        'init',
        *map(itemgetter(0), (task_count_or_url, params, infilevar, outfilevar, prompts, no_attempts_folder))))
    kwargs = dict(reduce(add, map(
        lambda x: list(x[1].items()),
        (task_count_or_url, params, infilevar, outfilevar, prompts, no_attempts_folder))))
    return s, kwargs


@patch('yandex_algorithms.cli.commands.init')
def test_init_command_accept_params(init_mock: Mock, init_str_with_kwargs: tuple[str, dict]):
    s, kwargs = init_str_with_kwargs
    args = s.split()
    main(args)
    init_mock.assert_called_once_with(**kwargs)


@pytest.fixture(params=('', 'A'), ids=('et', 't'))
def taskname(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'taskname': _split(s)}
    return s, v


@pytest.fixture(params=('', '-t 1', '--testnum 1', '-c A_MLE_1', '--compare A_MLE_1'), ids=('en', 'st', 'lt', 'sc', 'lc'))
def testnum(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    if s:
        if '-t' in s:
            v = {'testnum': int(_split(s)), 'errortaskname': None}  # type: ignore[arg-type] # есть проверка
        else:
            v = {'testnum': None, 'errortaskname': _split(s)}  # type: ignore[dict-item]
    else:
        v = {'testnum': None, 'errortaskname': None}
    return s, v


@pytest.fixture(params=('', '-vv'), ids=('ev', 'lv'))
def verbose(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'verbose': s.count('v')}
    return s, v


@pytest.fixture
def run_str_with_kwargs(taskname: tuple[str, dict], testnum: tuple[str, dict], verbose: tuple[str, dict], cleanup_imports):
    # def run_str_with_kwargs(taskname: str, testnum: str, verbose: str, example_dir: str, cleanup_imports):
    s = ' '.join((
        'run',
        *map(itemgetter(0), (taskname, testnum, verbose))))
    kwargs = dict(reduce(add, map(
        lambda x: list(x[1].items()),
        (taskname, testnum, verbose)))
    )
    return s, kwargs


@patch('yandex_algorithms.cli.commands.run')
def test_run_command_accept_params(run_mock: Mock, run_str_with_kwargs: tuple[str, dict]):
    s, kwargs = run_str_with_kwargs
    args = s.split()
    main(args)
    run_mock.assert_called_once_with(**kwargs)


@pytest.fixture(params=('', 'A'), ids=('en', 'n'))
def solution_name(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'solution_name': s or None}
    return s, v


@pytest.fixture(params=('', '-n', '--no-tests'), ids=('et', 'st', 'lt'))
def notests(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'run_tests': not bool(s)}
    return s, v


@pytest.fixture(params=('', '-w 1', '--wait-seconds 1'), ids=('ew', 'sw', 'lw'))
def wait_seconds(request: pytest.FixtureRequest) -> tuple[str, dict]:
    s = request.param
    v = {'wait_seconds': int(_split(s) or 0)}
    return s, v


@pytest.fixture
def send_str_with_kwargs(solution_name: tuple[str, dict], notests: tuple[str, dict], wait_seconds: tuple[str, dict]):
    s = ' '.join((
        'send',
        *map(itemgetter(0), (solution_name, notests, wait_seconds))))
    kwargs = dict(reduce(add, map(
        lambda x: list(x[1].items()),
        (solution_name, notests, wait_seconds)))
    )
    return s, kwargs


@patch('yandex_algorithms.cli.commands.send')
def test_send_command_accept_params(send_mock: Mock, send_str_with_kwargs: tuple[str, dict]):
    s, kwargs = send_str_with_kwargs
    args = s.split()
    main(args)
    send_mock.assert_called_once_with(**kwargs)


# def test_run_command_accept_params(run_str: str, capsys: pytest.CaptureFixture):
#     args = run_str.split()
#     main(args)
#     _, err = capsys.readouterr()
#     assert 'FAILED' not in err

# @pytest.fixture(params=(f"-t {_task_count}", f"--task-count {_task_count}"), ids=('st', 'lt'))
# def task_count(request: pytest.FixtureRequest) -> str:
#     return request.param

# @pytest.fixture(params=("", "-i inp", "--infilevar inp"), ids=('ei', 'si', 'li'))
# def infilevar(request: pytest.FixtureRequest) -> str:
#     return request.param

# @pytest.fixture(params=("", "-o inp", "--outfilevar out"), ids=('eo', 'so', 'lo'))
# def outfilevar(request: pytest.FixtureRequest) -> str:
#     return request.param

# @pytest.fixture(params=("", "-m '>;<", "--prompts '>>>;<<<'"), ids=('em', 'sm', 'lm'))
# def prompts(request: pytest.FixtureRequest) -> str:
#     return request.param

# @pytest.fixture(params=("", "-n", "--no-attempts-folder"), ids=('en', 'sn', 'ln'))
# def no_attempts_folder(request: pytest.FixtureRequest) -> str:
#     return request.param

# @pytest.fixture
# def init_taskcount_str_with_effect(no_attempts_folder: str, prompts: str, outfilevar: str,
#                  infilevar: str, task_count: str) -> Tuple[str, Tuple[int, bool, bool, bool]]:
#     s = ' '.join(('init', task_count, infilevar, outfilevar, prompts, no_attempts_folder))
#     effect = (
#         int(task_count.split()[1]),
#         infilevar.split()[1] if infilevar else "",
#         outfilevar.split()[1] if outfilevar else "",
#         no_attempts_folder != "",
#     )
#     return s, effect

# def test_init_command_task_count(init_taskcount_str_with_effect: Tuple[str, Tuple[int, bool, bool, bool]],
#                                  cwd: Path):
#     s, (task_count, invar, outvar, no_folder) = init_taskcount_str_with_effect
#     args = s.split()
#     main(args)
#     py_files = tuple(glob.glob(cwd.absolute().as_posix() + '/*.py'))
#     init_files = tuple(glob.glob(cwd.absolute().as_posix() + '/inputs/*'))
#     attempt_folder = (cwd / 'attempts')
#     assert len(py_files) == _task_count + 1 # + conftest.py
#     assert len(init_files) == _task_count
#     assert attempt_folder.exists() is not no_folder
#     parser = configparser.ConfigParser()
#     assert len(parser.read(cwd / config._CONFIG_FILE)) == 1
#     assert config._SECTION_NAME in parser.sections()
#     section = parser[config._SECTION_NAME]
#     assert section['prompt_in']
#     assert section['prompt_out']
#     assert section['infilevar'] == invar
#     assert section['outfilevar'] == outvar

# @pytest.fixture(params=(f"", f"A"), ids=('et', 't'))
# def taskname(request: pytest.FixtureRequest) -> str:
#     return request.param

# @pytest.fixture(params=("", "-t 1", "--testnum 1", "-c A_MLE_1", "--compare A_MLE_1"), ids=('en', 'st', 'lt', 'sc', 'lc'))
# def testnum(request: pytest.FixtureRequest) -> str:
#     return request.param

# @pytest.fixture(params=("", "-vv"), ids=('ev', 'lv'))
# def verbose(request: pytest.FixtureRequest) -> str:
#     return request.param

# @pytest.fixture
# def run_str(taskname: str, testnum: str, verbose: str, example_dir: str, cleanup_imports):
#     s = ' '.join(('run', taskname, testnum, verbose))
#     if taskname == '':
#         (example_dir / 'A.py').touch()
#     return s

# def test_run_command(run_str: str, capsys: pytest.CaptureFixture):
#     args = run_str.split()
#     main(args)
#     _, err = capsys.readouterr()
#     assert 'FAILED' not in err
