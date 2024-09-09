from enum import Enum

from oss.remote.remotes.buttonpad import ButtonpadRemote, ButtonpadHook
from oss.remote.remotes.keypad import KeypadRemote, KeypadHook


class RemoteType(Enum):
    KEYPAD: type[KeypadRemote] = KeypadRemote
    BUTTONPAD: type[ButtonpadRemote] = ButtonpadRemote


class HookType(Enum):
    KEYPAD: type[KeypadHook] = KeypadHook
    BUTTONPAD: type[ButtonpadHook] = ButtonpadHook
