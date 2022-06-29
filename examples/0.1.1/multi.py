import loggus
from concurrent.futures import ThreadPoolExecutor

name = "cza"
age = 12
loggus.SetFormatter(loggus.JsonFormatter)


def task():
    loggus.variables(
        name,
        age
    ).info("hello")


executor = ThreadPoolExecutor(max_workers=10)
for i in range(1000):
    executor.submit(task)
