import importlib
import logging
from itertools import islice
from pathlib import Path
from typing import Union

from . import modules
from .config import store_config
from .templates import CONFTEST, generate_main
from .unit import TestCompare, TestSolution
from .utils import (
    check_solution,
    copy_to_attempts,
    get_last_modified_file,
    infinite_name_generator,
    init_dir,
)

_logger = logging.getLogger(__name__)


def init(prompts: str, task_count: Union[int, None], infilevar: str,
         outfilevar: str, from_url: Union[str, None], params: list[str],
         no_attempts_folder: bool):
    prompt_in, prompt_out = prompts.split(';')
    if isinstance(task_count, int):
        inputs = [
            (name, '', '')
            for name in islice(infinite_name_generator(), task_count)
        ]
    elif isinstance(from_url, str):
        params_dict = {
            k: v
            for k, v in map(
                lambda x: x.split('=', 1),
                params
            )
        }
        mod = modules.init_module(from_url, **params_dict)
        inputs = mod.load_problems(prompt_in, prompt_out)
    init_dir('.', generate_main(infilevar, outfilevar), CONFTEST, no_attempts_folder, inputs)
    store_config(prompt_in=prompt_in, prompt_out=prompt_out, infilevar=infilevar, outfilevar=outfilevar)


def run(taskname: Union[str, None], testnum: Union[int, None], errortaskname: Union[str, None], verbose: int = 1):
    params = (taskname, testnum, errortaskname)
    if any(params):
        case_ = TestSolution if errortaskname is None else TestCompare
    else:
        try:
            mod = importlib.import_module('conftest')
            errortaskname_mod = getattr(mod, 'errortaskname', None)
            case_ = TestSolution if errortaskname_mod is None else TestCompare
        except ImportError:
            case_ = TestSolution
    check_solution(case_('test_solution'), taskname, testnum, errortaskname, verbose)


def send(solution_name: Union[str, None], run_tests: bool, wait_seconds: int):
    solution_name = solution_name or get_last_modified_file(Path('.'))
    if run_tests:
        if check_solution(TestSolution('test_solution'), solution_name, None, None) is False:
            return
    mod = modules.get_module()
    verdict, testnum = mod.send_submission(solution_name, wait_seconds)
    if verdict == mod.OK:
        _logger.info('✅ Good job! 👍')
    elif verdict == mod.NOT_READY:
        _logger.info('🤷 Not enough time. Passed %d test', testnum)
    else:  # ошибка
        _logger.info('❌ Got error at test number %d', testnum)
        copy_to_attempts(solution_name, verdict, testnum)
