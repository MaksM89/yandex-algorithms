import importlib
from pathlib import Path
from unittest import TestCase

from .config import load_config
from .utils import (
    get_last_modified_file,
    mock_input_output,
    readinout,
    store_input_output,
)


class TestSolution(TestCase):

    def setUp(self):
        try:
            conftest = importlib.import_module('conftest')
        except ModuleNotFoundError:
            conftest = object()
        if hasattr(self, 'params'):
            task, test, _ = self.params
            task = task or get_last_modified_file(Path('.'))
        elif conftest is not None:
            if hasattr(conftest, 'taskname'):
                task = conftest.taskname
            else:
                task = get_last_modified_file(Path('.'))
            test = getattr(conftest, 'testnum', None)
        else:  # ide
            task = get_last_modified_file(Path('.'))
            test = None
        assert task is not None, 'no .py files found'
        assert isinstance(task, str), 'task name must be a string'
        assert test is None or isinstance(test, int), 'test num must be None or int'
        self.cmp = getattr(conftest, f'compare_{task}', lambda exp, out, inp: self.assertMultiLineEqual(exp, out))
        self.mod = importlib.import_module(task)
        assert hasattr(self.mod, 'main'), 'solution must have main function'
        cfg = load_config()
        self.data = list(readinout(task, cfg['prompt_in'], cfg['prompt_out'], test))
        assert len(self.data), f'test {test} do not exists'
        self.infilevar = cfg['infilevar']
        self.outfilevar = cfg['outfilevar']

    def test_solution(self):
        for i, (inp, exp, testname) in enumerate(self.data, 1):
            with self.subTest(f'{self.mod.__name__}_{testname}'):
                out = ''
                with mock_input_output(self.mod, inp, self.infilevar, self.outfilevar) as mock_out:
                    self.mod.main()
                    out = mock_out.text
                self.cmp(exp, out, inp)


class TestCompare(TestCase):

    def setUp(self):
        try:
            conftest = importlib.import_module('conftest')
            if hasattr(self, 'params'):
                task, _, errortask = self.params
                task = task or get_last_modified_file(Path('.'))
                errortask = errortask or get_last_modified_file(Path('./attempts'))
            else:
                task = getattr(conftest, 'taskname', get_last_modified_file(Path('.')))
                errortask = getattr(conftest, 'errortaskname', get_last_modified_file(Path('./attempts')))
            self.gen = getattr(conftest, f'gen_{task}')
        except (ModuleNotFoundError, AttributeError):
            raise NotImplementedError(
                'To compare solutions, you need a test generator defined in conftest.py')
        cfg = load_config()
        assert task is not None, 'no .py files found'
        assert errortask is not None, 'no bad solution name provided'
        assert isinstance(task, str), 'task name must be a string'
        assert isinstance(errortask, str), 'task name must be a string'
        self.cmp = getattr(conftest, f'compare_{task}', lambda exp, out, inp: self.assertMultiLineEqual(exp, out))
        assert self.gen, 'No input generator provided'
        self.mod = importlib.import_module(task)
        assert hasattr(self.mod, 'main'), 'solution must have main function'
        self.error_mod = importlib.import_module(f'attempts.{errortask}')
        assert hasattr(self.error_mod, 'main'), 'solution must have main function'
        self.data = list(self.gen())
        assert len(self.data), 'No tests generated'
        self.infilevar = cfg['infilevar']
        self.outfilevar = cfg['outfilevar']

    def test_solution(self):
        for inp in self.data:
            self.cur_data = inp
            self.exp = None
            with mock_input_output(self.error_mod, inp, self.infilevar, self.outfilevar) as mock_out:
                self.error_mod.main()
                self.exp = mock_out.text
            out = ''
            with mock_input_output(self.mod, inp, self.infilevar, self.outfilevar) as mock_out:
                self.mod.main()
                out = mock_out.text
            self.cmp(self.exp, out, inp)
            self.cur_data = None
            self.exp = None

    def tearDown(self):
        if self.cur_data is not None and self.exp is not None:
            store_input_output(self.mod.__name__, self.cur_data, self.exp)
