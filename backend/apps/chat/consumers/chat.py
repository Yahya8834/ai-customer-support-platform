import json
from channels.generic.websocket import AsyncWebsocketConsumer



class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.workspace_uuid = self.scope["url_route"]["kwargs"][
            "workspace_uuid"
        ]

        self.group_name = f"workspace_{self.workspace_uuid}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

        await self.send(
            text_data="connected",
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "token": event["token"],
            }),
        )