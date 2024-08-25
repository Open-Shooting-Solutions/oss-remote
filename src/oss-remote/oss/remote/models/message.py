from oss.core.models.base.message import BaseBrokerConnection, BaseBrokerMessage


class BrokerConnection(BaseBrokerConnection):
    def send_command(self, command):
        self._send(broker_message="aaa")
