from channels.generic.websocket import AsyncWebsocketConsumer
import json

class RockPaperScissorsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.multiplayer_rps_room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.rps_room_name = "multiplayer_rps_%s" % self.multiplayer_rps_room_name

        self.room_state = {}

        self.attempts = 3 # initialise the number of attempts for this round

        global user1_name
        user1_name = ""

        global user2_name
        user2_name = ""

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
        global user1_name
        global user2_name

        self.room_state.setdefault('rps_options', {})
        self.room_state['rps_options'][username] = {
            "user_option" : user_option,
            "rps_outcome": ""
        }

        self.room_state.setdefault('attempts', 3)

        if len(self.room_state['rps_options']) == 2:


            for username in self.room_state['rps_options'].keys():
                if username != user:
                    user2_choice = self.room_state['rps_options'][username]['user_option']
                    user2_name = username
                else:
                    user1_choice = self.room_state['rps_options'][user]['user_option']
                    user1_name = user
                    

            if user1_choice != "" and user2_choice != "":

                if self.attempts > 0:
                    self.attempts -= 1

                    rps_outcomes = {
                        'rock' : {'paper' : 'lose', 'scissors' : 'win'},
                        'paper' : {'rock' : 'win', 'scissors' : 'lose'},
                        'scissors' : {'rock' : 'lose', 'paper' : 'win'}
                    }

                    rps_outcome_user_1 = rps_outcomes[user1_choice].get(user2_choice, 'draw')
                    rps_outcome_user_2 = rps_outcomes[user2_choice].get(user1_choice, 'draw')

                    self.room_state['rps_options'][user1_name] = {
                        "user_option" : user1_choice,
                        "rps_outcome": rps_outcome_user_1
                    }

                    self.room_state['rps_options'][user2_name] = {
                        "user_option" : user2_choice,
                        "rps_outcome": rps_outcome_user_2
                    }

                    #self.room_state['rps_options'] = {}

        await self.send(
            text_data=json.dumps(
                {
                    "user_list" : [user1_name, user2_name],
                    "rps_options": self.room_state['rps_options'],
                    "attempts" : self.attempts
                }
            )
        )
