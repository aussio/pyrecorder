import pynput
from models import *
from timer import ElapsedTimeThread


class BaseRecorder:

    listener: pynput._util.AbstractListener
    events: list[GUIEvent] = []
    timer: ElapsedTimeThread

    def __init__(self, timer=None):
        # currently unused
        self.timer = timer

    def start(self):
        self.listener.start()

    def stop(self):
        print("STOPPING LISTENER")
        self.listener.stop()

    def append_event(self, event: GUIEvent):
        """Append deduplicated events."""
        # TODO: how to check equality here?
        if self.events[-1] == event:
            pass
        else:
            self.events.append(event)
