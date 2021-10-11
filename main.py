import time
import pyautogui
import pickle
from pathlib import Path

from models import *
from timer import ElapsedTimeThread
from recorders.mouse import MouseRecorder
from recorders.keyboard import KeyboardRecorder


PYAUTOGUI_EVENT_PAUSE = 0.01
PYAUTOGUI_DARWIN_PAUSE = 0.001
RECORDINGS_PATH = Path(__file__).parent.resolve() / "recordings"


def parse_arguments():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--record",
        "-r",
        action="store",
        dest="record_filename",
        default="",
        help=f"The filename to store the recording within. Will be saved in {RECORDINGS_PATH}.",
    )
    group.add_argument(
        "--play",
        "-p",
        action="store",
        dest="play_filename",
        help=f"The filename to load and play. Files are loaded from {RECORDINGS_PATH}.",
    )
    parser.add_argument(
        "--duration",
        "-d",
        type=int,
        default=-1,
        help=f"The duration to record in milliseconds. -1 to record indefinitely - use 'ESC' key to stop.",
    )

    args = parser.parse_args()

    if not args.record_filename and not args.play_filename:
        parser.error("No action requested. Must use either --record or --play.\nSee --help for more information.")

    if args.play_filename and not Path.is_file(RECORDINGS_PATH / args.play_filename):
        parser.error(f"File not found at {RECORDINGS_PATH / args.play_filename}. Check again within {RECORDINGS_PATH}.")

    if args.duration == -1:
        args.duration = 60 * 60 * 24 * 7 * 1000  # 7 days in milliseconds

    return args


def record(record_filename, duration):
    timer = ElapsedTimeThread()
    mouse = MouseRecorder(timer=timer)
    keyboard = KeyboardRecorder(timer=timer)

    def start():
        timer.start()
        mouse.start()
        keyboard.start()

    def stop():
        timer.stop()
        mouse.stop()
        keyboard.stop()

    keyboard.on_esc = stop

    print("Recording! Press 'esc' key to stop.")

    start()

    while not timer.is_stopped() and timer.elapsedTime() < duration:
        time.sleep(1)

    stop()

    with open(RECORDINGS_PATH / record_filename, "wb") as f:
        pickle.dump(mouse.events, f)

    print(f"Done! Saved within {RECORDINGS_PATH / args.record_filename}!")


def playback(playback_filename):

    with open(RECORDINGS_PATH / playback_filename, "rb") as f:
        events = pickle.load(f)

    print(f"REPLAYING! Total events: {len(events)}")
    pyautogui.PAUSE = PYAUTOGUI_EVENT_PAUSE
    pyautogui.DARWIN_CATCH_UP_TIME = PYAUTOGUI_DARWIN_PAUSE

    for index, event in enumerate(events):
        playback_event(event)
        try:
            time.sleep(get_sleep(event, events[index + 1]))
        except IndexError:
            pass


def playback_event(event):
    # print(f"id:{event['id']}:time:{event['time']}", flush=True)
    if event["type"] == EVENT_TYPE.MOUSE_MOVE:
        pyautogui.moveTo(event["coordinates"]["x"], event["coordinates"]["y"])
    elif event["type"] == EVENT_TYPE.MOUSE_CLICK:
        x, y = event["coordinates"]["x"], event["coordinates"]["y"]
        # print(f"click:{event['id']}", x, y)
        pyautogui.click(
            x,
            y,
        )


def get_sleep(current_event, next_event):
    return (next_event["time"] - current_event["time"]) / 1000


if __name__ == "__main__":

    import argparse

    args = parse_arguments()

    if args.record_filename:
        record(args.record_filename, args.duration)
    elif args.play_filename:
        playback(args.play_filename)
    else:
        print("Unknown args.")
