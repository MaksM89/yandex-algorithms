from unittest.mock import Mock, patch

import pytest

from yandex_algorithms import unit
from yandex_algorithms.commands import init, run, send


@patch('yandex_algorithms.commands.init_dir')
@patch('yandex_algorithms.commands.store_config')
@patch('yandex_algorithms.commands.modules')
def test_init_use_task_count(mod_mock: Mock, sc_mock: Mock, id_mock: Mock):
    task_count = 3
    prompt_in = '>'
    prompt_out = '<'
    infilevar, outfilevar = '', ''
    init(prompt_in + ';' + prompt_out, task_count, infilevar, outfilevar, None, [], True)
    inputs = id_mock.call_args_list[0].args[-1]
    assert len(inputs) == task_count
    assert mod_mock.init_module.call_count == 0
    assert mod_mock.load_problems.call_count == 0
    sc_mock.assert_called_once_with(prompt_in=prompt_in, prompt_out=prompt_out,
                                    infilevar=infilevar, outfilevar=outfilevar)


@patch('yandex_algorithms.commands.init_dir')
@patch('yandex_algorithms.commands.store_config')
@patch('yandex_algorithms.commands.modules')
def test_init_use_from_url(mod_mock: Mock, sc_mock: Mock, id_mock: Mock):
    from_url = 'url'
    prompt_in = '>'
    prompt_out = '<'
    params = {'a': 'b', 'c': 'd'}
    params_list = list(map('='.join, params.items()))
    # mod_init_mock = Mock()
    # mod_mock.init_module.return_value = mod_init_mock
    # mod_init_mock.assert_called_once_with(from_url, **params)
    inputs = [('', '', '') for _ in range(5)]
    mod_mock.load_prolems.return_value = inputs
    infilevar, outfilevar = '', ''
    init(prompt_in + ';' + prompt_out, None, infilevar, outfilevar, from_url, params_list, True)
    mod_mock.init_module.assert_called_once_with(from_url, **params)
    mod_mock.init_module.return_value.load_problems.assert_called_once_with(prompt_in, prompt_out)
    sc_mock.assert_called_once_with(prompt_in=prompt_in, prompt_out=prompt_out,
                                    infilevar=infilevar, outfilevar=outfilevar)


@pytest.mark.parametrize(
    'case_class,taskname,testnum,errortaskname',
    (
        pytest.param(unit.TestSolution, None, None, None, id='all_none'),
        pytest.param(unit.TestSolution, 'A', 1, None, id='all_none'),
        pytest.param(unit.TestCompare, 'A', None, 'A_MLE_1', id='all_none'),
    )
)
@patch('yandex_algorithms.commands.check_solution')
def test_run_command(run_tests_mock: Mock, case_class, taskname, testnum, errortaskname):
    case_instance = case_class('test_solution')
    run(taskname, testnum, errortaskname)
    run_tests_mock.assert_called_once_with(case_instance, taskname, testnum, errortaskname, 1)


@patch('yandex_algorithms.commands.copy_to_attempts')
@patch('yandex_algorithms.commands.check_solution')
@patch('yandex_algorithms.commands.modules')
def test_send_can_send_and_store(mod_mock: Mock, run_mock: Mock, copy_mock: Mock):
    solution_name, run_tests, wait_seconds, verdict, test_num = 'A', True, 30, 'MLE', 1
    mod_mock.get_module.return_value.send_submission.return_value = (verdict, test_num)
    send(solution_name, run_tests, wait_seconds)
    run_mock.assert_called_once()
    mod_mock.get_module.assert_called_once()
    mod_mock.get_module.return_value.send_submission.assert_called_once_with(solution_name, wait_seconds)
    copy_mock.assert_called_once_with(solution_name, verdict, test_num)
