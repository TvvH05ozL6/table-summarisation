from datetime import datetime
from typing import Dict

from mantistablex.process.utils.channels.channel import Channel


class Console(Channel):
    def __init__(self, table_id):
        super().__init__(table_id, "chat")  # TODO: Change name to console

    def info(self, message):
        self.send({
            'type': 'console_message',
            'message': message,
            'message_type': 'info',
        })

    def error(self, message):
        self.send({
            'type': 'console_message',
            'message': message,
            'message_type': 'error',
        })

    def send(self, body: Dict):
        # Default value
        if "datetime" not in body.keys():
            body["datetime"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        super().send(body)
