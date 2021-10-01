import time
import threading


class ElapsedTimeThread(threading.Thread):
    """ "Stoppable thread that prints the time elapsed"""

    def __init__(self):
        super(ElapsedTimeThread, self).__init__()
        self._stop_event = threading.Event()
        self.thread_start = time.time()

    def stop(self):
        self._stop_event.set()
        self.join()

    def is_stopped(self):
        return self._stop_event.is_set()

    def elapsedTime(self):
        return time.time() - self.thread_start

    def printElapsedTime(self):
        print("\rElapsed Time {:.3f} s. ".format(self.elapsedTime()), end="", flush=True)

    def run(self):
        self.thread_start = time.time()
        while not self.is_stopped():
            self.printElapsedTime()
            # include a delay here so the thread doesn't uselessly thrash the CPU
            time.sleep(0.01)
