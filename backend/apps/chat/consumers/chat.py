import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.chat.tasks import process_chat_message
from channels.db import database_sync_to_async
from apps.chat.models.message import Message



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

    @database_sync_to_async
    def save_user_message(self, conversation_uuid, content):
        return Message.objects.create(
            conversation_id=conversation_uuid,
            role="user",
            content=content,
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        await self.save_user_message(
            conversation_uuid=data["conversation_uuid"],
            content=data["prompt"],
        )

        process_chat_message.delay(
            workspace_uuid=str(self.workspace_uuid),
            provider=data["provider"],
            model=data["model"],
            prompt=data["prompt"],
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "token": event["token"],
            }),
        )