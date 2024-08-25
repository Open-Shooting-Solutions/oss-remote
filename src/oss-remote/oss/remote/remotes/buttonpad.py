from enum import Enum
from oss.remote.models.remote import BaseRemote
from oss.remote.models.remote import TimerAction


# Need to implement logging
class ButtonpadAction(Enum):
    GPIO1: TimerAction = TimerAction.TOGGLE_PHASE
    GPIO2: TimerAction = TimerAction.RESET_PHASE
    GPIO3: TimerAction = TimerAction.PREVIOUS_PHASE
    GPIO4: TimerAction = TimerAction.NEXT_PHASE


class ButtonpadRemote(BaseRemote):
    def __init__(self) -> None:
        pass

    def _register_hooks(self) -> None:
        pass

    def _remove_hooks(self) -> None:
        pass
