from textwrap import dedent

from .utils import is_valid_variable_name


def generate_main(infilevar: str = '', outfilevar: str = '') -> str:
    lines = []
    if is_valid_variable_name(infilevar):
        lines.append(f"{infilevar} = 'input.txt'")
    if is_valid_variable_name(outfilevar):
        lines.append(f"{outfilevar} = 'output.txt'")
    if lines:
        lines.append('')  # добавит перенос строки
    MAIN = dedent("""
            {header}
            def main():
                pass

            if __name__ == '__main__':
                main()
        """
                  )
    header = '\n'.join(lines)
    return MAIN.format(header=header).lstrip()


CONFTEST = dedent(
    """
    from yandex_algorithms.unit import TestSolution, TestCompare

    # taskname = 'A'
    # testnum = None
    # errortaskname = A_SLOW

    # example of compare function signature
    # def compare_A(exp: str, out: str, inp: str):
    #     assert exp == out, 'Strings are not equal'

    # example of generator signature for sum two numbers
    # def gen_A(): # -> Generator[str, None, None]
    #     from random import randint
    #     n = 10
    #     for _ in range(n):
    #         a, b = randint(1, 5), randint(-4, 4)
    #         yield f'{a} {b}\\n'

    """).lstrip()
