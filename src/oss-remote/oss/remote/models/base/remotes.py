from enum import Enum
from oss.remote.models.base.remote import BaseRemote
from oss.remote.remotes.gpio import GPIORemote


class Remote(Enum):
    GPIO: GPIORemote = GPIORemote
