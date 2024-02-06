from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RockPaperScissorsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.multiplayer_rps_room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.rps_room_name = "multiplayer_rps_%s" % self.multiplayer_rps_room_name

        await self.channel_layer.group_add(self.rps_room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        print(f"WebSocket Disconnected with code: {close_code}")
        await self.channel_layer.group_discard(self.rps_room_name, self.channel_name)

    async def receive(self, text_data):
        print(f"Received raw data: {text_data}")

        try:
            data = json.loads(text_data)
            message = data['message']
            username = data["username"]
            
            await self.channel_layer.group_send(
                self.rps_room_name,
                {
                    "type" : "rps_move",
                    "message" : message,
                    "username" : username
                },
            )

        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    
    async def rps_move(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username" : username
                }
            )
        )
