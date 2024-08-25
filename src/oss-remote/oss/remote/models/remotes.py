from enum import Enum
from oss.remote.remotes.buttonpad import ButtonpadRemote
from oss.remote.remotes.keypad import KeypadRemote


class Remote(Enum):
    KEYPAD: KeypadRemote = KeypadRemote
    GPIO: ButtonpadRemote = ButtonpadRemote
