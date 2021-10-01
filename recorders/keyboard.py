from pynput import keyboard as pykeyboard
from recorders.base import BaseRecorder


class KeyboardRecorder(BaseRecorder):

    ESCAPE_KEY = pykeyboard.Key.esc

    def __init__(self, on_esc=lambda: None, timer=None):
        super().__init__()
        self.listener = pykeyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.on_esc = on_esc

    def on_press(self, key):
        try:
            print("alphanumeric key {0} pressed".format(key.char))
        except AttributeError:
            print("special key {0} pressed".format(key))

    def on_release(self, key):
        print("{0} released".format(key))
        if key == self.ESCAPE_KEY:
            self.on_esc()
