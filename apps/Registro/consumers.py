from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AccessConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('Hay conexion: ', self.channel_name)
        await self.accept()
        await self.channel_layer.group_add(
            "access_socket",  # The name of the group
            self.channel_name
        )

    async def disconnect(self, close_code):
        print(f'Se cerro la conexion:{close_code}')

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json['status']

        # sender = text_data_json['sender']
        # print(data, sender)

        await self.send(text_data=json.dumps({
            'status':data,
            #'sender':sender
        }))
    
    async def accessStatus(self, event):
        data = event['data']
        print('Data: ', data)
        await self.send(text_data=json.dumps({
            'consumerStatus': data
        }))
