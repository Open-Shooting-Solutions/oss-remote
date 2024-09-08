from enum import Enum
from dataclasses import dataclass
from oss.core.models.base.remote import BaseRemote, BaseHook
from oss.core.models.base.timer import TimerControl


# Need to implement logging
class ButtonpadAction(Enum):
    GPIO1: TimerControl = TimerControl.TOGGLE_PHASE
    GPIO2: TimerControl = TimerControl.RESET_PHASE
    GPIO3: TimerControl = TimerControl.PREVIOUS_PHASE
    GPIO4: TimerControl = TimerControl.NEXT_PHASE


@dataclass
class ButtonpadHook(BaseHook):
    pin: str
    action: TimerControl


class ButtonpadRemote(BaseRemote):
    pass
