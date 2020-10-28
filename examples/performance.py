import time
from typing import List

from talipp.indicators import SMA


class Timer(object):
    def __init__(self, name: str = "") -> None:
        self.name = name

        self.start_tmstmp_ms = None

    def __enter__(self) -> None:
        self.start_tmstmp_ms = time.time_ns()

    def __exit__(self, type, value, traceback) -> None:
        print(f'Timer {self.name} finished. Took {round((time.time_ns() - self.start_tmstmp_ms)/1000000, 3)} ms.')


def gen_values(num: int) -> List[int]:
    return [i for i in range(0, num)]


def measure(values_n: int, indicator, *args):
    print(f"Calculate {indicator.__name__}{args} from {values_n:,} values")
    values = gen_values(values_n)
    with Timer():
        indicator(*args, values)


def test_sma():
    measure(1000, SMA, 10)
    measure(100000, SMA, 10)
    measure(1000000, SMA, 10)

    measure(1000, SMA, 200)
    measure(100000, SMA, 200)
    measure(1000000, SMA, 200)


if __name__ == "__main__":
    test_sma()
