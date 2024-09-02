from enum import Enum
from oss.core.models.base.remote import BaseRemote
from oss.core.models.base.timer import TimerControl


# Need to implement logging
class ButtonpadAction(Enum):
    GPIO1: TimerControl = TimerControl.TOGGLE_PHASE
    GPIO2: TimerControl = TimerControl.RESET_PHASE
    GPIO3: TimerControl = TimerControl.PREVIOUS_PHASE
    GPIO4: TimerControl = TimerControl.NEXT_PHASE


class ButtonpadRemote(BaseRemote):
    def __init__(self) -> None:
        pass

    def _register_hooks(self) -> None:
        pass

    def _remove_hooks(self) -> None:
        pass
