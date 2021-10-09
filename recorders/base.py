import pynput
from models import *
from timer import ElapsedTimeThread


SAMPLING_RATE = 50
"""The millisecond amount at which we deduplicate events.

I haven't found how to reduce the sampling rate from `pynput` in the
Recorders, so this replicates that same effect by not writing down all events.
"""


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
        if len(self.events) == 0:
            self.events.append(event)
        else:
            if event["type"] == EVENT_TYPE.MOUSE_CLICK:
                self.events.append(event)
            elif event["type"] == EVENT_TYPE.MOUSE_MOVE:
                last_rounded_time = self._round(self.events[-1]["time"])
                current_rounded_time = self._round(event["time"])
                if last_rounded_time == current_rounded_time:
                    pass
                else:
                    self.events.append(event)

    def _round(self, time: float):
        return round(time / SAMPLING_RATE)
