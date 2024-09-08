from enum import Enum
from symtable import Class

from oss.remote.remotes.buttonpad import ButtonpadRemote, ButtonpadHook
from oss.remote.remotes.keypad import KeypadRemote, KeypadHook


class RemoteType(Enum):
    KEYPAD: KeypadRemote = KeypadRemote
    GPIO: ButtonpadRemote = ButtonpadRemote


class HookType(Enum):
    KEYPAD: KeypadHook = KeypadHook
    GPIO: ButtonpadHook = ButtonpadHook
