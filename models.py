from __future__ import annotations
from typing import TypedDict
from enum import Enum, auto


class EVENT_TYPE(Enum):
    MOUSE_MOVE = auto()
    MOUSE_CLICK = auto()


class GUIEvent(TypedDict):
    id: int  # for troubleshooting
    type: EVENT_TYPE
    time: float
    coordinates: Coordinates
    down: bool
    up: bool


class Coordinates(TypedDict):
    x: float
    y: float
