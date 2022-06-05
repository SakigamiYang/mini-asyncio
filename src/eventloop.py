# coding: utf-8
import heapq
import time
import collections


class EventLoop:
    def __init__(self):
        self._ready = collections.deque()
        self._scheduled = list()
        self._stopping = False

    def call_soon(self, callback, *args, **kwargs):
        self._ready.append((callback, args, kwargs))

    def call_later(self, delay, callback, *args, **kwargs):
        t = time.time() + delay
        heapq.heappush(self._scheduled, (t, callback, args, kwargs))

    def stop(self):
        self._stopping = True

    def run_forever(self):
        while True:
            self.run_once()
            if self._stopping:
                break

    def run_once(self):
        # scheduled tasks
        now = time.time()
        while self._scheduled:
            # check the time of the minimum item in the heap
            if self._scheduled[0][0] > now:
                break

            _, callback, args, kwargs = heapq.heappop(self._scheduled)
            self._ready.append((callback, args, kwargs))

        # ready tasks
        num_task = len(self._ready)
        for i in range(num_task):
            callback, args, kwargs = self._ready.popleft()
            callback(*args, **kwargs)
