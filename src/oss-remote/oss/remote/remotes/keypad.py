import keyboard
from enum import Enum
from oss.remote.models.base.remote import BaseRemote


# Need to implement logging
class KeypadAction(enum):
    S: str = "startpauze"
    T: str = "stop"
    R: str = "reset"


class KeypadRemote(BaseRemote):
    pass
