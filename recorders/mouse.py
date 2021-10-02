from pynput import mouse as pymouse

from models import *
from recorders.base import BaseRecorder


class MouseRecorder(BaseRecorder):
    def __init__(self, timer=None):
        super().__init__(timer=timer)
        self.listener = pymouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)

    def on_move(self, x, y):
        print("Pointer moved to {0}".format((x, y)))
        self.append_event(
            GUIEvent(
                type=EVENT_TYPE.MOUSE_MOVE,
                time=self.timer.elapsedTime(),
                coordinates=Coordinates(x=round(x), y=round(y)),
            )
        )

    def on_click(self, x, y, button, pressed):
        print("{0} at {1}".format("Pressed" if pressed else "Released", (x, y)))
        self.append_event(
            GUIEvent(
                type=EVENT_TYPE.MOUSE_CLICK,
                time=self.timer.elapsedTime(),
                coordinates=Coordinates(x=round(x), y=round(y)),
            )
        )

    def on_scroll(self, x, y, dx, dy):
        print("Scrolled {0} at {1}".format("down" if dy < 0 else "up", (x, y)))
