import time
from typing import List

import numpy
import talib

from talipp.indicators import SMA, StochRSI, TEMA


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


def measure(values_n: int, indicator, **args):
    print(f"Calculate {indicator.__name__}{args} from {values_n:,} values")
    values = numpy.random.random(values_n)
    with Timer():
        indicator(**args, input_values = values)


def measure_sma(values_n: int, period: int):
    close = numpy.random.random(values_n)

    start = time.time_ns()
    output = SMA(period, close)
    output[-1]
    t1 = (time.time_ns() - start) / 1000000

    start = time.time_ns()
    output = talib.SMA(close, timeperiod = period)
    output[-1]
    t2 = (time.time_ns() - start) / 1000000

    t3 = 0.0
    output = None
    for i in range(period, values_n):
        close = numpy.random.random(i)
        start = time.time_ns()
        output = talib.SMA(close, timeperiod = period)
        t3 += (time.time_ns() - start) / 1000000

    print(f"SMA({period});{values_n:,};{round(t1, 3)};{round(t2, 3)};{round(t3, 3)}")


def measure_tema(values_n: int, period: int):
    close = numpy.random.random(values_n)

    start = time.time_ns()
    output = TEMA(period, close)
    output[-1]
    t1 = (time.time_ns() - start) / 1000000

    start = time.time_ns()
    output = talib.TEMA(close, timeperiod = period)
    output[-1]
    t2 = (time.time_ns() - start) / 1000000

    t3 = 0.0
    output = None
    for i in range(period, values_n):
        close = numpy.random.random(i)
        start = time.time_ns()
        output = talib.TEMA(close, timeperiod = period)
        t3 += (time.time_ns() - start) / 1000000

    print(f"TEMA({period});{values_n:,};{round(t1, 3)};{round(t2, 3)};{round(t3, 3)}")


def measure_stochrsi(values_n: int, period: int, k_period: int, d_period: int):
    close = numpy.random.random(values_n)

    start = time.time_ns()
    output = StochRSI(period, period, k_period, d_period, close)
    output[-1]
    t1 = (time.time_ns() - start) / 1000000

    start = time.time_ns()
    output = talib.STOCHRSI(close, timeperiod = period, fastk_period=k_period, fastd_period=d_period)
    output[-1]
    t2 = (time.time_ns() - start) / 1000000

    t3 = 0.0
    output = None
    for i in range(period, values_n):
        close = numpy.random.random(i)
        start = time.time_ns()
        output = talib.STOCHRSI(close, timeperiod = period, fastk_period=k_period, fastd_period=d_period)
        t3 += (time.time_ns() - start) / 1000000

    print(f"StochRSI({period},{k_period},{d_period});{values_n:,};{round(t1, 3)};{round(t2, 3)};{round(t3, 3)}")


if __name__ == "__main__":
    for i in range(1000, 50000, 500):
        measure_sma(i, 20)

    for i in range(1000, 50000, 500):
        measure_tema(i, 20)

    for i in range(1000, 50000, 500):
        measure_stochrsi(i, 14, 3, 3)