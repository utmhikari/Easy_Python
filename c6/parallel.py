from multiprocessing import Pool
from threading import Thread
import datetime
import functools
import asyncio

TOTAL = 20000


def task(n):
    end = -n
    while n > end:
        n -= 1


def sequential():
    for i in range(TOTAL):
        task(i)


def multi_process():
    pool = Pool(10)
    pool.map(task, range(TOTAL))


async def async_io():
    async def async_task(n):
        task(n)
    await asyncio.gather(*[async_task(i) for i in range(TOTAL)])


def multi_thread():
    def tasks(ns):
        for n in ns:
            task(n)
    threads = []
    inputs = [[] for _ in range(10)]
    for i in range(TOTAL):
        inputs[(i % 10)].append(i)
    for i in range(10):
        threads.append(Thread(target=functools.partial(tasks, inputs[i])))
        threads[-1].start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    # sequential
    start = datetime.datetime.now()
    sequential()
    print("Sequential: %s" % (datetime.datetime.now() - start).total_seconds())
    # multi-process
    start = datetime.datetime.now()
    multi_process()
    print("Multi-Process: %s" % (datetime.datetime.now() - start).total_seconds())
    # asyncio
    start = datetime.datetime.now()
    asyncio.run(async_io())
    print("Async-IO: %s" % (datetime.datetime.now() - start).total_seconds())
    # multi-thread
    start = datetime.datetime.now()
    multi_thread()
    print("Multi-Thread: %s" % (datetime.datetime.now() - start).total_seconds())
