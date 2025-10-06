from collections.abc import Iterable

from yandex_algorithms.unit import TestSolution

# taskname = 'A'
# testnum = None
# errortaskname = None

# # example of compare_ signature
# def compare_A(exp: str, out: str, inp: str):
#     assert exp == out, 'Strings are not equal'

# example of gen_ signature


def gen_A() -> Iterable[str]:
    return (f'{i} {i}' for i in range(3))
