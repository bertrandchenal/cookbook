import bisect
import sys
from contextlib import contextmanager
from time import perf_counter


def pretty_nb(number):
    prefixes = "yzafpnum_kMGTPEZY"
    factors = [1000**i for i in range(-8, 8)]
    if number == 0:
        return 0
    if number < 0:
        return "-" + pretty_nb(-number)
    idx = bisect.bisect_right(factors, number) - 1
    prefix = prefixes[idx]
    return "%.2f%s" % (number / factors[idx], "" if prefix == "_" else prefix)


@contextmanager
def timeit(title=""):
    start = perf_counter()
    yield
    delta = perf_counter() - start
    print(title, pretty_nb(delta) + "s", file=sys.stderr)


if __name__ == "__main__":
    from time import sleep
    from random import random, randint
    with timeit("Sleep Demo"):
        sleep(random()**(randint(1, 10)))
