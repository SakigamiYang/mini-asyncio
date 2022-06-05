# coding: utf-8
class Future:
    def __init__(self, eventloop):
        self._loop = eventloop
        self._result = None
        self._done = False
        self._callbacks = list()

    def set_result(self, result):
        if self._done:
            raise RuntimeError('future already done')
        self._result = result
        self._done = True

        for cb in self._callbacks:
            self._loop.call_soon(cb)

    def get_result(self):
        if self._done:
            return self._result
        raise RuntimeError('future ')

    def add_done_callback(self, callback):
        self._callbacks.append(callback)

    def done(self):
        return self._done

    def __await__(self):
        yield self
        return self.get_result()
