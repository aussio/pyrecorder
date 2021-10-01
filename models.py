from __future__ import annotations
from typing import TypedDict
from enum import Enum, auto


class EVENT_TYPE(Enum):
    MOUSE_MOVE = auto()
    MOUSE_CLICK = auto()


class GUIEvent(TypedDict):
    type: EVENT_TYPE
    time: float
    coordinates: Coordinates


class Coordinates(TypedDict):
    x: float
    y: float
