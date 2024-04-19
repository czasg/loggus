# coding: utf-8
import loggus
import time

from loggus.utils import Mark, process

mark = Mark()

with mark.mark("total"):
    with mark.mark("svc_cost"):
        total = 200
        for i in range(total + 1):
            process(i, total=total, progress=">")
            time.sleep(0.1)

    with mark.mark("rds_cost"):
        total = 30
        for i in range(total + 1):
            process(i, total=total, progress="-")
            time.sleep(0.1)

    with mark.mark("sql_cost"):
        total = 20
        for i in range(total + 1):
            process(i, total=total, progress_length=60)
            time.sleep(0.1)

loggus.update(mark).info("ok")
