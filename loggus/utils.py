# coding: utf-8
import time
import contextlib


class Mark(dict):
    """
    >>> mark = Mark()
    >>> with mark.mark("svc_cost"):
    >>>     time.sleep(3)
    >>> with mark.mark("rds_cost"):
    >>>     time.sleep(2)
    >>> with mark.mark("sql_cost"):
    >>>     time.sleep(1)
    """

    @contextlib.contextmanager
    def mark(self, field: str):
        start = time.time()
        yield
        self[field] = f"{time.time() - start:.2f}"


def process(cur: int, total=100, progress="#", progress_length=50, description=""):
    """
    >>> total = 200
    >>> for i in range(total+1):
    >>>     process(i, total)
    >>>     time.sleep(0.1)
    """
    ratio = cur / total
    dynamic_ratio = int(ratio * progress_length)
    dynamic = progress * dynamic_ratio + ' ' * (progress_length - dynamic_ratio)
    message = f"\r{description}[{dynamic}] {cur}/{total} - {int(ratio * 100)}%"
    end = ""
    if ratio == 1:
        end = "\n"
    print(message, end=end)
