import io
import keyword
import logging
import logging.handlers
import os
import random
import re
import string
import tempfile
import unittest
from collections.abc import Generator
from contextlib import contextmanager, redirect_stdout
from itertools import combinations_with_replacement as cmbr
from pathlib import Path
from queue import Queue
from string import ascii_uppercase
from typing import Any, Union
from unittest.mock import patch

from .config import load_config

_logger = logging.getLogger(__name__)


class ParseFileException(Exception):

    def __init__(self, file: Path, lineno: int, message: str):
        self.file = file
        self.lineno = lineno
        self.message = message

    def __str__(self):
        if self.lineno > 0:
            return f'Wrong file format: {self.file.name} line {self.lineno}: {self.message}'
        return f'Wrong file format: {self.file.name}: {self.message}'


def _add_input_output(g: Union[re.Match, None], buf: list) -> Union[str, None]:
    if g is not None:
        testfile = (Path.cwd() / 'inputs' / g.groups()[0]).absolute()
        if not testfile.exists():
            return f'"{testfile}" do not exists'
        line = testfile.read_text()
        if not line.endswith('\n'):
            line += '\n'
        buf.append(line)
    return None


def readinout(filename: str, prompt_in: str, prompt_out: str, testnum=None) -> Generator[tuple[str, str, str], None, None]:
    filepath = Path.cwd().absolute() / 'inputs' / filename
    assert filepath.exists(), f'The file "{filepath}" does not exists'
    filepattern = re.compile(r'-f\s+(?P<file>\S+)')
    namepattern = re.compile(r'-n\s+(?P<name>[A-Za-z_]+)')
    testname = ''
    with open(filepath) as f:
        inp: list[str] = []
        out: list[str] = []
        buf = None
        curtest = 0
        for lineno, line in enumerate(f, 1):
            if line.startswith(prompt_in):
                if buf is inp:
                    raise ParseFileException(filepath, lineno, f'second time got "{prompt_in}"')
                elif buf is out:
                    if len(out) != 0:
                        if testnum is None or testnum == curtest:
                            yield ''.join(inp), ''.join(out), testname
                    else:
                        raise ParseFileException(filepath, lineno, 'output must have a string (maybe empty)')
                curtest += 1
                inp.clear()
                out.clear()
                buf = inp
                g = namepattern.search(line)
                if g is None:
                    testname = f'test_{curtest}'
                else:
                    testname = g.groups()[0]
                if (error := _add_input_output(filepattern.search(line), buf)):
                    raise ParseFileException(filepath, lineno, error)
            elif line.startswith(prompt_out):
                if buf is not inp:
                    raise ParseFileException(filepath, lineno, f'second time got "{prompt_out}"')
                elif len(inp) == 0:
                    raise ParseFileException(filepath, lineno, 'input must have a string (maybe empty)')
                buf = out
                if (error := _add_input_output(filepattern.search(line), buf)):
                    raise ParseFileException(filepath, lineno, error)
            elif buf is not None:
                if not line.endswith('\n'):  # no empty row at the end of file
                    line += '\n'
                buf.append(line)
            else:
                raise ParseFileException(filepath, lineno, f'expected start with "{prompt_in}", got {line}')
        if len(inp) == 0 or len(out) == 0:
            raise ParseFileException(filepath, -1, 'is empty or incomplete')
        if testnum is None or testnum == curtest:
            yield ''.join(inp), ''.join(out), testname


class Wrapper:

    def __init__(self, stream: io.StringIO, file: Union[tempfile._TemporaryFileWrapper, None]):
        self._stream = stream
        self._filename = file.name if file is not None else None

    @property
    def text(self) -> str:
        text = self._stream.getvalue()
        if text == '' and isinstance(self._filename, str):
            text = Path(self._filename).read_text()
        return text


@contextmanager
def mock_input_output(module, inp: str, infilevar: str, outfilevar: str) -> Generator[Wrapper, None, None]:
    i = io.StringIO(inp)
    patches: list = [
        patch('sys.stdin', i),
    ]
    if hasattr(module, 'stdin'):
        patches.append(patch(f'{module.__name__}.stdin', i))
    if hasattr(module, f'{infilevar}'):
        fin = tempfile.NamedTemporaryFile(delete=False)
        fin.write(inp.encode())
        fin.close()
        patches.append(patch(f'{module.__name__}.{infilevar}', fin.name))
    else:
        fin = None
    if hasattr(module, f'{outfilevar}'):
        fout = tempfile.NamedTemporaryFile(delete=False)
        fout.close()
        patches.append(patch(f'{module.__name__}.{outfilevar}', fout.name))
    else:
        fout = None
    for p in patches:
        p.start()
    with redirect_stdout(io.StringIO()) as out:
        if hasattr(module, 'stdout'):
            patches.append(patch(f'{module.__name__}.stdout', out))
            patches[-1].start()
        yield Wrapper(out, fout)
    for p in patches:
        p.stop()
    if fin:
        os.remove(fin.name)
    if fout:
        os.remove(fout.name)


def get_last_modified_file(path: Path) -> str:
    assert path.exists() and path.is_dir()
    files = tuple(
        filter(
            lambda x: x.suffix == '.py' and x.stem != 'conftest',
            path.iterdir()
        )
    )
    assert len(files), 'No py files found'
    last_file = max(files, key=lambda p: p.stat().st_mtime)
    return last_file.stem


def infinite_name_generator():
    i = 1
    while True:
        yield from map(''.join, cmbr(ascii_uppercase, i))
        i += 1


def init_dir(dirname: str, main_content: str, conftest_content: Union[str, None],
             no_attempts_folder: bool = False, inputs: list[tuple[str, str, str]] = []):
    cur = Path(dirname)
    if not (cur.exists() and cur.is_dir()):
        raise ValueError(f'Expected existing dir, got {dirname}')
    input_folder = cur / 'inputs'
    input_folder.mkdir(exist_ok=True)
    if not no_attempts_folder:
        (cur / 'attempts').mkdir(exist_ok=True)
        _logger.info('The folder attempts has been created')
    if conftest_content is not None:
        (cur / 'conftest.py').write_text(conftest_content)
        _logger.info('The file conftest.py has been created')
    for name, _, input in inputs:
        pyfile = cur / f'{name}.py'
        if not pyfile.exists():
            pyfile.write_text(main_content)
            _logger.debug('The file %s.py has been created', name)
        else:
            _logger.warning('The file %s.py exists not been modified', name)
        infile = cur / 'inputs' / f'{name}'
        if not infile.exists():
            infile.write_text(input)
            _logger.debug('The file inputs/%s has been created', name)
        else:
            _logger.warning('The file inputs/%s exists and not been modified', name)


def check_solution(case_: unittest.TestCase, taskname: Union[str, None], testnum: Union[int, None],
                   errortaskname: Union[str, None], verbosity: int = 1) -> bool:
    params = (taskname, testnum, errortaskname)
    if any(params):
        setattr(case_, 'params', params)
    suite = unittest.TestSuite()
    suite.addTest(case_)
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    return result.wasSuccessful()


def copy_to_attempts(alias: str, err: str, test_num: int):
    attempts_folder = Path('attempts')
    if attempts_folder.exists():
        # копируем решение
        name = f'{alias}_{err}_{test_num}'
        old_file = Path(f'{alias}.py')
        new_file = attempts_folder / f'{name}.py'
        for i in range(1000):
            if new_file.exists():
                new_file = attempts_folder / f'{name}_{i + 1}.py'
            else:
                break
        new_file.write_bytes(old_file.read_bytes())
        _logger.info('Copied solution to %s', new_file.as_posix())


def store_input_output(alias: str, inp: str, out: str, id_: str = ''):
    if not inp.endswith('\n'):
        inp += '\n'
    if not out.endswith('\n'):
        out += '\n'
    cfg = load_config()
    id_ = id_ or ''.join(random.choices(string.ascii_letters, k=12))
    infile = Path('inputs') / f'{alias}_{id_}_in'
    infile.write_text(inp)
    outfile = Path('inputs') / f'{alias}_{id_}_out'
    outfile.write_text(out)
    prompt_in = cfg['prompt_in']
    prompt_out = cfg['prompt_out']
    if inp.count('\n') > 10:
        p_in = prompt_in + f' -f {infile.name}\n'
    else:
        p_in = prompt_in + '\n' + inp
    if out.count('\n') > 10:
        p_out = prompt_out + f' -f {infile.name}\n'
    else:
        p_out = prompt_out + '\n' + out
    text = p_in + p_out
    with open(f'inputs/{alias}', 'a') as f:
        f.write(text)
    _logger.info('Stored input/output in inputs/%s', alias)


def is_valid_variable_name(name: Any) -> bool:
    if not isinstance(name, str) or not name:
        return False
    if keyword.iskeyword(name):
        return False
    if name[0].isdigit():
        return False
    return re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', name) is not None


def init_logger() -> logging.handlers.QueueListener:
    logger = logging.getLogger(__package__)
    del logger.handlers[:]
    fmt = logging.Formatter('%(asctime)s >> %(message)s', '%H:%M:%S')
    hndl = logging.StreamHandler()
    hndl.setFormatter(fmt)
    queue: Queue = Queue()
    logger.addHandler(logging.handlers.QueueHandler(queue))
    listner = logging.handlers.QueueListener(queue, hndl)
    if os.environ.get('YALGO_DEBUG_ON'):
        logger.setLevel('DEBUG')
    else:
        logger.setLevel('INFO')
    listner.start()
    return listner
