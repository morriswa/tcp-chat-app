
from typing import Any

__token: str | None = None
__window: Any = None
__frames: dict = {}


def get_token() -> str:
    global __token
    return __token


def set_token(token: str) -> None:
    global __token
    __token = token


def delete_token():
    global __token
    __token = None


def get_window() -> Any:
    global __window
    return __window


def set_window(w):
    global __window
    __window = w


def set_frame(name, frame):
    global __window
    __frames[name] = frame


def get_frame(name) -> Any:
    global __frames
    return __frames.get(name)
