from enum import Enum
from typing import Tuple, Callable
import keyboard
from oss.core.log import Log
from oss.core.message import BrokerMessage, BrokerConnection, BrokerExchangeType
from oss.core.models.base.remote import BaseRemote
from oss.core.models.base.timer import TimerControl

# Activate module wide logging
logger = Log.get_logger_function()(__name__)


# Need to implement logging
class KeypadAction(Enum):
    Q: TimerControl = TimerControl.TOGGLE_PHASE
    W: TimerControl = TimerControl.RESET_PHASE
    E: TimerControl = TimerControl.RESET_STAGE


class KeypadRemote(BaseRemote):
    _configured_hooks: list[Tuple[str, TimerControl, Callable[[], None]]] = []

    def __init__(self) -> None:
        self._broker_connection = BrokerConnection(host="localhost", port=5672)
        self._broker_connection.setup_channel(name="remote", exchange_type=BrokerExchangeType.TOPIC)
        self._register_hooks()

    def __del__(self):
        self._remove_hooks()

    def _handle_hook_event(self, action: TimerControl) -> None:
        broker_message: BrokerMessage = BrokerMessage(
            producer=self._identifier,
            body={"action": action.value},
        )
        broker_message.send(
            broker_connection=self._broker_connection,
            exchange="remote",
            routing_key="remote.keypad.action",
            broker_message=broker_message,
        )

    def _register_hooks(self) -> None:
        for keypad_action in KeypadAction:
            hook_remove_function: Callable[[], None] = keyboard.add_hotkey(
                hotkey=keypad_action.name,  # Name is a reference to the KEY of the Enum KV
                callback=self._handle_hook_event,  # The function to be called on keypress
                args=[keypad_action.value],  # The arguments passed to the function
                timeout=0.1,
            )
            self._configured_hooks.append((keypad_action.name, keypad_action.value, hook_remove_function))

    def _remove_hooks(self) -> None:
        keyboard.unhook_all_hotkeys()
