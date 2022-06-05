# coding: utf-8
import random
import threading
import time
from future import Future
from task import Task
from eventloop import EventLoop

total_blocking_time = 0.
random.seed(time.time())


async def one_task():
    print(f'begin task')
    print(f'    begin big_step')
    big_result = await big_step()
    print(f'    end big_step with {big_result}')
    print(f'end task')


async def big_step():
    print(f'        begin small_step')
    small_result = await small_step()
    print(f'        end small_step with {small_result}')
    return small_result * 1000


async def small_step():
    global loop
    future = Future(loop)
    fake_io_read(future)
    result = await future
    return result


def fake_io_read(future):
    def read():
        global total_blocking_time

        sleep_time = random.random()
        total_blocking_time += sleep_time
        time.sleep(sleep_time)  # simulate an I/O blocking
        future.set_result(random.randint(1, 100))

    threading.Thread(target=read).start()


def until_all_done(eventloop, tasks):
    tasks = list(filter(lambda t: not t.done(), tasks))
    if tasks:
        loop.call_soon(until_all_done, eventloop, tasks)
    else:
        loop.stop()


if __name__ == '__main__':
    loop = EventLoop()
    tasks = [Task(loop, one_task()) for i in range(100)]

    start = time.time()

    loop.call_later(1, until_all_done, loop, tasks)
    loop.run_forever()

    print(f'total blocking: {total_blocking_time}, real blocking: {time.time() - start}')
