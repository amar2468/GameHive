from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RockPaperScissorsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print(f"WebSocket Disconnected with code: {close_code}")

    async def receive(self, text_data):
        print(f"Received raw data: {text_data}")

        try:
            data = json.loads(text_data)
            message = data['content']
            print(f"Received message: {message}")

            await self.send(text_data=json.dumps({
                'message': 'Message received and processed successfully.'
            }))
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
