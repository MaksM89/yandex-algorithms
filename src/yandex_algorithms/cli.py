import argparse
from operator import eq
from typing import Union

from . import commands


def prompt_str(value):
    splitted = value.split(';')
    if len(splitted) != 2 or eq(*splitted):
        raise argparse.ArgumentTypeError('Значения промптов должны быть разделены ";" и отличаться')
    return value


def positive_int(value):
    """Проверяет, что значение — натуральное число"""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Значение '{value}' не является натуральным числом")
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f'Значение должно быть положительным, а не {ivalue}')
    return ivalue


def create_parser():
    # Создаём парсер для основной команды
    parser = argparse.ArgumentParser(
        prog='yalgo',
        description='Утилита yalgo для решения задач в контестах.',
        epilog="""Примеры:
        yalgo init -t 5
        yalgo run A -t 3
        yalgo send A -nw 60""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')

    subparsers = parser.add_subparsers(
        title='Команды',
        dest='command',
        help='Описание команд',
        required=True
    )

    # ----------команда `init`----------------------
    parser_init = subparsers.add_parser(
        'init',
        help='Создать в каталоге необходимую структуру с py-файлами',
    )

    group = parser_init.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-t', '--task-count',
        type=positive_int,
        help='Количество задач',
        metavar='POSITIVE_INT'
    )

    group.add_argument(
        '-u', '--from-url',
        type=str,
        help='url адрес контеста',
    )

    parser_init.add_argument(
        '-p', '--param',
        action='append',
        dest='params',
        help='Параметры, необходимые при использовании --from-url',
        default=[],
        metavar='key=value'
    )

    parser_init.add_argument(
        '-i', '--infilevar',
        type=str,
        help="Имя переменной для входного файла (например, 'input_file')",
        default=''
    )

    parser_init.add_argument(
        '-o', '--outfilevar',
        type=str,
        help="Имя переменной для выходного файла (например, 'output_file')",
        default=''
    )

    parser_init.add_argument(
        '-m', '--prompts',
        type=prompt_str,
        help="Разделители в файле для ввода/вывода через ';'",
        default='-->;<--',
        metavar='-->;<--',
    )

    parser_init.add_argument(
        '-n', '--no-attempts-folder',
        action='store_true',
        help='Не создавать папку для неудачных попыток',
        default=False
    )

    parser_init.set_defaults(func=commands.init)

    # ----------команда `run`----------------------
    parser_run = subparsers.add_parser(
        'run',
        description='команда для тестирования решения',
        help='Запустить тесты для решения',
    )

    parser_run.add_argument(
        'taskname',
        nargs='?',
        type=str,
        help='названия файла без расширения .py (например, А)'
    )

    group = parser_run.add_mutually_exclusive_group(required=False)

    group.add_argument(
        '-t', '--testnum',
        type=positive_int,
        help='номер теста для запуска'
    )

    group.add_argument(
        '-c', '--compare',
        type=str,
        help='название решения в папке attempts без .py (например, A_MLE_5)',
        dest='errortaskname',
    )

    parser_run.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='уровень детализации'
    )

    parser_run.set_defaults(func=commands.run)

    # ---------- команда send -------------
    parser_send = subparsers.add_parser(
        'send',
        description='команда для посылки решения (необходима инициализация модуля при помощи init --from-url)',
        help='Отправить решение',
    )

    parser_send.add_argument(
        'solution_name',
        nargs='?',
        type=str,
        help='Названия файла без расширения .py (например, А)'
    )

    parser_send.add_argument(
        '-n', '--no-tests',
        dest='run_tests',
        action='store_false',
        help='Не запускать тесты перед отправкой'
    )

    parser_send.add_argument(
        '-w', '--wait-seconds',
        type=int,
        default=0,
        help='Время ожидания вердикта в секундах'
    )

    parser_send.set_defaults(func=commands.send)

    return parser


def main(argv: Union[list[str], None] = None):
    p = create_parser()
    args = vars(p.parse_args(argv))
    args.pop('command')
    callback = args.pop('func')
    callback(**args)
