# coding: utf-8
import itertools

from future import Future

_task_id_counter = itertools.count(1)


class Task(Future):
    def __init__(self, eventloop, coro):
        super().__init__(eventloop)
        self.coro = coro
        self._id = f'Task-{next(_task_id_counter)}'
        self._loop.call_soon(self.run)

    def run(self):
        print(f'----- {self._id} -----')
        if not self._done:
            try:
                x = self.coro.send(None)
            except StopIteration as e:
                self.set_result(e.value)
            else:
                assert isinstance(x, Future)
                x.add_done_callback(self.run)
        else:
            print('task is done')
