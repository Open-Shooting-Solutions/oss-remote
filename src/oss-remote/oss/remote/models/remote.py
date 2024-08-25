from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID, uuid4
from oss.core.message import BrokerConnection


# Shouldnt this be a timer control instead of action?
class TimerControl(Enum):
    TOGGLE_PHASE: str = "TOGGLE_STAGE"
    RESET_PHASE: str = "STOP_PHASE"
    NEXT_PHASE: str = "NEXT_PHASE"
    PREVIOUS_PHASE: str = "PREVIOUS_PHASE"
    RESET_STAGE: str = "RESET_STAGE"
    NEXT_STAGE: str = "NEXT_STAGE"
    PREVIOUS_STAGE: str = "PREVIOUS_STAGE"
    SET_DELAY: str = "SET_DELAY"


class BaseRemote(ABC):
    # Each remote needs an uuid so we can keep track of which remote triggered an action.
    # This is mostly for debugging.
    _identifier: UUID = uuid4()

    # Each remote needs an connection to the message broker to send commands
    _broker_connection: BrokerConnection

    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def __del__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _handle_hook_event(self, action: TimerControl) -> None:
        raise NotImplementedError

    @abstractmethod
    def _register_hooks(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _remove_hooks(self) -> None:
        raise NotImplementedError
