import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat_app.models import UserChat


class ChatConsumer(AsyncWebsocketConsumer):
   
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        # Join room group

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        room_name=text_data_json["room_name"]
        user_name=text_data_json["username"]
        # await self.save_message(message,room_name,user_name)
        group=room_name.split(".")
        group.sort()
        print(group)
        print(self.channel_layer)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message",
                                   "message": self.user.username + ' : ' + message,
                                   "sender":self.user.username,
                                   "group_name":self.room_name
                                   }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @sync_to_async
    def save_message(self,message,room_name,user_name):
        UserChat.objects.create(message=message,group_name=room_name,user=user_name)


