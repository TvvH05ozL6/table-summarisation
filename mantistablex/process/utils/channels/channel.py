from typing import Dict

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Channel:
    def __init__(self, channel_id, name: str):
        self.channel_id = channel_id
        self.name = name

    def send(self, body: Dict):
        async_to_sync(get_channel_layer().group_send)(
            f'{self.name}_{self.channel_id}',
            body
        )
