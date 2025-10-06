import re
from pathlib import Path
from unittest.mock import Mock

import pytest

from yandex_algorithms import unit


@pytest.fixture
def setparams(monkeypatch: pytest.MonkeyPatch, example_dir: Path) -> tuple[str, int, str]:
    taskname, testnum, errortaskname = 'B', 5, 'B_TL_17'
    monkeypatch.setattr(
        'importlib.import_module',
        Mock(side_effect=lambda *args: Mock(spec_set=['main', 'args'], args=args))
    )
    monkeypatch.setattr(
        'yandex_algorithms.unit.readinout',
        Mock(side_effect=lambda *args: args)
    )
    return taskname, testnum, errortaskname


@pytest.fixture
def setconftst(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, example_dir: Path, cleanup_imports) -> tuple[str, int, str]:
    taskname, testnum, errortaskname = 'A', 5, 'A_MLE_1'
    conf = tmp_path / 'conftest.py'
    with open('conftest.py') as f:
        code = f.read()
    code = re.sub(r'^# (?!.*example)(.*)$', r'\1', code, flags=re.MULTILINE)
    code = re.sub(r'\btaskname\s*=\s*(\S+)', f'taskname = "{taskname}"', code, flags=re.MULTILINE)
    code = re.sub(r'testnum\s*=\s*(\S+)', f'testnum = {testnum}', code, flags=re.MULTILINE)
    code = re.sub(r'\berrortaskname\s*=\s*(\S+)', f'errortaskname = "{errortaskname}"', code, flags=re.MULTILINE)
    code = re.sub(r'assert\s*(\S+)\s*==\s*(\S+)', r'assert \1 != \2', code, flags=re.MULTILINE)
    # code += dedent("""
    #     def gen_A():
    #         return (f'{i} {i}' for i in range(1, 3))
    #     """)
    conf.write_text(code)
    monkeypatch.syspath_prepend(tmp_path)
    monkeypatch.setattr(
        'yandex_algorithms.unit.readinout',
        Mock(side_effect=lambda *args: args)
    )
    return taskname, testnum, errortaskname


def test_solution_setup_from_params(setparams: tuple[str, int, str]):
    taskname, testnum, _ = setparams
    inst = unit.TestSolution()
    inst.params = (taskname, testnum, None)  # type: ignore[attr-defined]
    inst.setUp()
    assert taskname == inst.mod.args[0]
    assert taskname == inst.data[0]
    assert testnum == inst.data[-1]
    assert hasattr(inst, 'cmp')
    inst.cmp('a', 'a', 'no_input')
    assert hasattr(inst, 'infilevar')
    assert hasattr(inst, 'outfilevar')


def test_solution_setup_from_conftest(setconftst: tuple[str, int, str]):
    taskname, testnum, _ = setconftst
    inst = unit.TestSolution()
    inst.setUp()
    assert inst.mod.__name__ == taskname
    assert taskname == inst.data[0]
    assert testnum == inst.data[-1]
    assert hasattr(inst, 'cmp')
    with pytest.raises(AssertionError):
        inst.cmp('a', 'a', 'no_input')
    assert hasattr(inst, 'infilevar')
    assert hasattr(inst, 'outfilevar')


def test_compare_setup_from_params_raise_error(setparams: tuple[str, int, str]):
    inst = unit.TestCompare()
    inst.params = (setparams[0], None, setparams[2])  # type: ignore[attr-defined]
    with pytest.raises(NotImplementedError) as e:
        inst.setUp()
    assert 'you need a test generator' in str(e.value)


def test_compare_setup_from_conftest(setconftst: tuple[str, int, str]):
    taskname, _, errortaskname = setconftst
    inst = unit.TestCompare()
    inst.setUp()
    assert taskname == inst.mod.__name__
    assert errortaskname == inst.error_mod.__name__.split('.')[1]
    assert hasattr(inst, 'cmp')
    with pytest.raises(AssertionError):
        inst.cmp('a', 'a', 'no_input')
    assert hasattr(inst, 'infilevar')
    assert hasattr(inst, 'outfilevar')
