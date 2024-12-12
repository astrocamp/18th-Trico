import json
from channels.generic.websocket import AsyncWebsocketConsumer

USER_CHANNELS = {}

class ChatConsumer (AsyncWebsocketConsumer) :
    async def connect (self):
        user_id = self.scope['user'].id

        USER_CHANNELS[user_id] = self.channel_name
        
        await self.accept()


    async def disconnect(self, close_code):
        user_id = self.scope['user'].id

        if user_id in USER_CHANNELS:
            del USER_CHANNELS[user_id]

    
    async def recive(self, text_data):

        text_data_json = json.load(text_data)

        target_user_id = text_data_json['tatget_user_id']
        message = text_data_json['message']
    
        target_channel_name = USER_CHANNELS.get(target_user_id)

        if target_channel_name:

            await self.channel_layer.send(
                target_channel_name,
                {
                    "type": "chat.message",
                    "message": message,
                }
            )
    

