from typing import Optional
from oss.remote.models.base.remote import BaseRemote
from oss.remote.models.base.remotes import Remote
from oss.core.models.base.app import BaseApp

# implement logging


class BuzzerApp(BaseApp):
    _remotes: list[BaseRemote] = []

    def __init__(self, remotes: Optional[list[Remote]]) -> None:
        # If there are remotes as a parameter, add them to the remotes list.
        if remotes:
            for remote in remotes:
                self._remotes.append(remote.value)
        else:
            # We have a major problem a remote app without a remote
            pass

    def run(self) -> None:
        # Create a connection to the message broker
        pass

    def terminate(self) -> None:
        # Terminate old connections to the message broker
        pass
