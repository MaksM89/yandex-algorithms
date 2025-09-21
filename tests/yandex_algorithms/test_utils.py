import glob
import importlib
import random
import time
from collections.abc import Generator
from itertools import zip_longest
from pathlib import Path
from textwrap import dedent
from typing import Union

import pytest

from yandex_algorithms.config import load_config
from yandex_algorithms.templates import generate_main
from yandex_algorithms.utils import (
    ParseFileException,
    check_solution,
    get_last_modified_file,
    init_dir,
    mock_input_output,
    readinout,
)

TwoStrings = tuple[str, str]


@pytest.fixture
def good_input(example_dir: Path) -> str:
    return 'A'


@pytest.fixture
def prompts(example_dir: Path) -> TwoStrings:
    config = load_config()
    return config['prompt_in'], config['prompt_out']


@pytest.fixture(
    params=(
        'emptyfile',
        'no_output',
        'no_input',
        'double_input',
        'double_output',
        'wrong_file',
    )
)
def bad_input(request: pytest.FixtureRequest, example_dir: Path, prompts: TwoStrings) -> Generator[str, None, None]:
    pin, pout = prompts
    inp = {
        'emptyfile': '',
        'no_output': f'{pin}\n 1 2\n',
        'no_input': f'1 2\n{pout}\n2',
        'double_input': f'{pin}\n 1 2\n{pin}\n 1 2\n',
        'double_output': f'{pin}\n 1 2\n{pout}\n2\n{pout}\n2\n',
        'wrong_file': f'{pin} -f not_exists\n{pout}\n2'
    }
    content = inp[request.param]
    name = 'A_bad'
    file = example_dir / 'inputs' / name
    file.write_text(content)
    yield name
    file.unlink()


@pytest.fixture(
    params=(
        ('', ''),
        ('inputfile', ''),
        ('', 'outputfile'),
        ('inputfile', 'outputfile')
    ),
    ids=('no_files', 'in', 'out', 'inout')
)
def inout_vars(request: pytest.FixtureRequest, cleanup_imports) -> TwoStrings:
    return request.param


@pytest.fixture
def task_file_name(inout_vars: TwoStrings, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    if inout_vars[0] == '':
        instr = 'a = input()'
    else:
        instr = f"with open({inout_vars[0]}, 'r') as f:\n        a = f.readline().rstrip()"
    if inout_vars[1] == '':
        outstr = 'print(a)'
    else:
        outstr = f"with open({inout_vars[1]}, 'w') as f:\n        f.write(a + '\\n')"
    code = generate_main(*inout_vars)
    code = code.replace('pass', f'{instr}\n    {outstr}')
    monkeypatch.syspath_prepend(tmp_path)
    file = tmp_path / 'A.py'
    file.write_text(code)
    return 'A'


@pytest.mark.parametrize(
    'inputs',
    ((('A', '', 'aaa'), ('B', '', 'dsads')), tuple()),
    ids=('tests', 'no_tests')
)
@pytest.mark.parametrize(
    'no_attempts_folder', (True, False), ids=('attempts', 'no_attempts')
)
@pytest.mark.parametrize(
    'conftest_content', ('import some', None), ids=('conftest', 'no_conftest')
)
def test_init_dir(conftest_content: Union[str, None], no_attempts_folder: bool,
                  inputs: list[tuple[str, str, str]], tmp_path: Path):
    MAIN_CONTENT = 'print(Hi)'
    cur_dir = tmp_path.absolute().as_posix()
    init_dir(cur_dir, MAIN_CONTENT, conftest_content, no_attempts_folder, inputs)
    assert (len(list(glob.glob(cur_dir + '/conftest.py'))) == 0) is (conftest_content is None)
    assert (len(list(glob.glob(cur_dir + '/attempts'))) == 0) is no_attempts_folder
    py_files = sorted(filter(lambda x: 'conftest.py' not in x, glob.glob(cur_dir + '/*.py')))
    assert len(inputs) == len(py_files)
    for filename, (alias, _, input) in zip_longest(py_files, inputs):
        assert Path(filename).stem == alias
        infile = tmp_path / 'inputs' / alias
        assert infile.exists()
        assert infile.read_text() == input


@pytest.mark.parametrize('testnum', (None, 3), ids=('all_test', 'one_test'))
def test_readinout_read_file(testnum: Union[int, None], good_input: str, prompts: TwoStrings):
    data = list(readinout(good_input, *prompts, testnum))
    if testnum is None:
        assert len(data) > 1
        assert data[0][2] == 'test_1'
    else:
        assert len(data) == 1
        assert data[0][2] != 'test_1'


def test_readinout_raise_error(bad_input: str, prompts: TwoStrings):
    with pytest.raises(ParseFileException):
        _ = list(readinout(bad_input, *prompts))


def test_readinout_raise_assert_error(example_dir: Path, prompts: TwoStrings):
    with pytest.raises(AssertionError):
        _ = list(readinout('bad_file', *prompts))


def test_mock_input_output(task_file_name: str, inout_vars: TwoStrings):
    inp = exp = '123\n'
    mod = importlib.import_module(task_file_name)
    with mock_input_output(mod, inp, *inout_vars) as mock_out:
        mod.main()
        out = mock_out.text
    assert exp == out


def test_get_last_modified_file(tmp_path: Path):
    for i in map(str, range(5)):
        (tmp_path / f'{i}.py').touch()
        time.sleep(0.01)  # для уникальности времени
    last_exp = str(random.randint(0, 4))
    (tmp_path / f'{last_exp}.py').write_text('last modified')
    (tmp_path / 'conftest.py').touch()
    last = get_last_modified_file(tmp_path)
    assert last_exp == last


def test_run_tests_run_solution(example_dir: Path, capsys: pytest.CaptureFixture):
    from yandex_algorithms.unit import TestSolution
    check_solution(TestSolution('test_solution'), 'A', None, None)
    _, err = capsys.readouterr()
    assert 'FAILED' not in err


def test_run_tests_run_compare(example_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture):
    from yandex_algorithms.unit import TestCompare
    conf = tmp_path / 'conftest.py'
    with open('conftest.py') as f:
        code = f.read()
    code += dedent("""
        def gen_A():
            return (f'{i} {i}' for i in range(1, 3))
        """)
    conf.write_text(code)
    monkeypatch.syspath_prepend(tmp_path)
    check_solution(TestCompare('test_solution'), 'A', None, 'A_MLE_1')
    _, err = capsys.readouterr()
    assert 'FAILED' not in err
