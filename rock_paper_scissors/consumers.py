from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
from gamehive.models import GameUserProfile
from asgiref.sync import sync_to_async

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

        global user1_wins
        user1_wins = 0

        global user2_wins
        user2_wins = 0

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

        global user1_wins
        global user2_wins

        self.room_state.setdefault('rps_options', {})
        self.room_state['rps_options'][username] = {
            "user_option" : user_option,
            "outcome_of_the_round": "",
            "total_wins" : 0
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

                    rps_outcomes = {
                        'rock' : {'paper' : 'lose', 'scissors' : 'win'},
                        'paper' : {'rock' : 'win', 'scissors' : 'lose'},
                        'scissors' : {'rock' : 'lose', 'paper' : 'win'}
                    }

                    rps_outcome_user_1 = rps_outcomes[user1_choice].get(user2_choice, 'draw')
                    rps_outcome_user_2 = rps_outcomes[user2_choice].get(user1_choice, 'draw')

                    if rps_outcome_user_1 == "win":
                        user1_wins += 1
                        self.attempts -= 1 # only reduce the number of attempts left if either user won
                    
                    elif rps_outcome_user_2 == "win":
                        user2_wins += 1
                        self.attempts -= 1 # only reduce the number of attempts left if either user won
                    
                    if self.attempts == 0:
                        if user1_wins > user2_wins:
                            rps_outcome_user_1 = "Game Over! You won this round! You have received 10 points!"
                            rps_outcome_user_2 = "Game Over! You failed to win this game! Good luck next time!"
                            
                            try:
                                user_instance = await sync_to_async(User.objects.get)(username=user1_name)
                                game_user_profile = await sync_to_async(GameUserProfile.objects.get)(user=user_instance)
                                game_user_profile.current_score += 10
                                await sync_to_async(game_user_profile.save)()
                            except GameUserProfile.DoesNotExist:
                                user_instance = await sync_to_async(User.objects.get)(username=user1_name)
                                game_user_profile = await sync_to_async(GameUserProfile.objects.get)(user=user_instance)
                                game_user_profile.current_score += 10
                                await sync_to_async(game_user_profile.save)()
                        elif user2_wins > user1_wins:
                            rps_outcome_user_1 = "Game Over! You failed to win this game! Good luck next time!"
                            rps_outcome_user_2 = "Game Over! You won this round! You have received 10 points!"

                            try:
                                user_instance_2 = await sync_to_async(User.objects.get)(username=user2_name)
                                game_user_profile = await sync_to_async(GameUserProfile.objects.get)(user=user_instance_2)
                                game_user_profile.current_score += 10
                                await sync_to_async(game_user_profile.save)()
                            except GameUserProfile.DoesNotExist:
                                user_instance_2 = await sync_to_async(User.objects.get)(username=user2_name)
                                game_user_profile = await sync_to_async(GameUserProfile.objects.get)(user=user_instance_2)
                                game_user_profile.current_score += 10
                                await sync_to_async(game_user_profile.save)()

                    self.room_state['rps_options'][user1_name] = {
                        "user_option" : user1_choice,
                        "outcome_of_the_round": rps_outcome_user_1,
                        "total_wins" : user1_wins
                    }

                    self.room_state['rps_options'][user2_name] = {
                        "user_option" : user2_choice,
                        "outcome_of_the_round": rps_outcome_user_2,
                        "total_wins" : user2_wins
                    }

                    await self.send(
                        text_data=json.dumps(
                            {
                                "user_list" : [user1_name, user2_name],
                                "rps_options": self.room_state['rps_options'],
                                "attempts" : self.attempts
                            }
                        )
                    )

                    self.room_state['rps_options'] = {}