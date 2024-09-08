from oss.core.log import Log
from oss.core.models.base.remote import BaseRemote
from oss.remote.remotes.type import RemoteType
from oss.core.models.base.app import BaseApp

# Activate module wide logging
logger = Log.get_logger_function()(__name__)


class RemoteApp(BaseApp):
    _remotes: list[BaseRemote] = []

    def __init__(self, remotes: list[RemoteType]) -> None:
        # Check if there are remotes as parameter
        if not remotes:
            # We have a major problem a remote app without a remote
            # implement logging
            logger.critical("No remotes provided as parameter")
            self.terminate()

        # If there are remotes as a parameter, add them to the remotes list.
        for remote in remotes:
            self._remotes.append(remote.value())

    def __del__(self):
        self.terminate()

    def run(self) -> None:
        while True:
            # don't have much to do right now :)
            pass

    def terminate(self) -> None:
        pass


app: BaseApp = RemoteApp(remotes=[RemoteType.KEYPAD])
app.run()
