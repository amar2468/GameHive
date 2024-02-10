from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RockPaperScissorsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.multiplayer_rps_room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.rps_room_name = "multiplayer_rps_%s" % self.multiplayer_rps_room_name

        self.room_state = {}

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
            user_option = data["user_option"]
            
            await self.channel_layer.group_send(
                self.rps_room_name,
                {
                    "type" : "rps_move",
                    "message" : message,
                    "user_option" : user_option,
                    "username" : username
                },
            )

        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    
    async def rps_move(self, event):
        user = str(self.scope["user"])
        user_option = event["user_option"]
        username = event["username"]

        self.room_state.setdefault('rps_options', {})
        self.room_state['rps_options'][username] = user_option

        if len(self.room_state['rps_options']) == 2:

            for username, choice in self.room_state['rps_options'].items():
                if username != user:
                    user2_choice = choice
                    user2_name = username
                else:
                    user1_choice = choice
                    user1_name = user
                    

            if user1_choice != "" and user2_choice != "":

                rps_outcomes = {
                    'rock' : {'paper' : 'lose', 'scissors' : 'win'},
                    'paper' : {'rock' : 'win', 'scissors' : 'lose'},
                    'scissors' : {'rock' : 'lose', 'paper' : 'win'}
                }

                rps_outcome = rps_outcomes[user1_choice].get(user2_choice, 'draw')

                print(rps_outcome)              

                print(user1_name, user1_choice)
                print(user2_name, user2_choice)

            self.room_state['rps_options'] = {}

        await self.send(
            text_data=json.dumps(
                {
                    "payload" : event
                }
            )
        )
