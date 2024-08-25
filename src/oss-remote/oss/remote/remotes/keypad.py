from enum import Enum
from typing import Tuple, Callable
import keyboard
from oss.core.log import Log
from oss.core.message import BrokerMessage, BrokerConnection, BrokerExchangeType
from oss.remote.models.remote import BaseRemote
from oss.remote.models.remote import TimerAction

# Activate module wide logging
logger = Log.get_logger_function()(__name__)


# Need to implement logging
class KeypadAction(Enum):
    Q: TimerAction = TimerAction.TOGGLE_PHASE
    W: TimerAction = TimerAction.RESET_PHASE
    E: TimerAction = TimerAction.RESET_STAGE


class KeypadRemote(BaseRemote):
    _configured_hooks: list[Tuple[str, TimerAction, Callable[[], None]]] = []

    def __init__(self) -> None:
        self._broker_connection = BrokerConnection(host="localhost", port=5672)
        self._broker_connection.setup_channel(name="remote", exchange_type=BrokerExchangeType.TOPIC)
        self._register_hooks()

    def __del__(self):
        self._remove_hooks()

    def _handle_hook_event(self, action: TimerAction) -> None:
        broker_message: BrokerMessage = BrokerMessage(
            broker_connection=self._broker_connection,
            exchange="remote",
            routing_key="remote.keypad.action",
            producer=self._identifier,
            body={"action": action},
        )
        broker_message.send()

    def _register_hooks(self) -> None:
        for action in KeypadAction:
            hook_remove_function: Callable[[], None] = keyboard.add_hotkey(
                hotkey=action.name,  # Name is a reference to the KEY of the Enum KV
                callback=self._handle_hook_event,  # The function to be called on keypress
                args=[action.value],  # The arguments passed to the function
                timeout=0.1,
            )
            self._configured_hooks.append((action.name, action.value, hook_remove_function))

    def _remove_hooks(self) -> None:
        keyboard.unhook_all_hotkeys()
