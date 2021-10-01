import time
import pyautogui

from models import *
from timer import ElapsedTimeThread
from recorders.mouse import MouseRecorder
from recorders.keyboard import KeyboardRecorder


RUN_TIME = 5
PYAUTOGUI_EVENT_PAUSE = 0.01
PYAUTOGUI_DARWIN_PAUSE = 0.001


if __name__ == "__main__":

    timer = ElapsedTimeThread()
    mouse = MouseRecorder()
    keyboard = KeyboardRecorder()

    def start():
        timer.start()
        mouse.start()
        keyboard.start()

    def stop():
        timer.stop()
        mouse.stop()
        keyboard.stop()

    keyboard.on_esc = stop

    start()

    while not timer.is_stopped() and timer.elapsedTime() < RUN_TIME:
        time.sleep(1)

    stop()

    print("REPLAYING!")
    time.sleep(2)

    pyautogui.PAUSE = 0.01
    pyautogui.DARWIN_CATCH_UP_TIME = 0.002
    for event in mouse.mouse_events:
        if event["type"] == EVENT_TYPE.MOUSE_MOVE:
            print(event)
            pyautogui.moveTo(event["coordinates"]["x"], event["coordinates"]["y"])