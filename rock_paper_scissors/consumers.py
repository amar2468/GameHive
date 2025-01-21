from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
from gamehive.models import GameUserProfile
from asgiref.sync import sync_to_async
import random

class RockPaperScissorsConsumer(AsyncWebsocketConsumer):
    # Creating a global list to hold all the available rooms (Rooms that have one player waiting)
    global available_rooms
    available_rooms = []

    async def connect(self):
        # If there are no players in any room, then generate a random room for the user to enter in.
        if not available_rooms:
            rps_room_name = random.randint(1,100)

            rps_room_name = str(rps_room_name)

            self.rps_room_name = rps_room_name

            available_rooms.append(self.rps_room_name)
        
        # If there are available rooms (Rooms that have one player waiting), add the user to the first available one.
        else:
            self.rps_room_name = available_rooms.pop(0)
        
        print(self.rps_room_name)

        self.room_state = {}

        self.attempts = 3 # initialise the number of attempts for this round

        await self.channel_layer.group_add(self.rps_room_name, self.channel_name)

        await self.accept()

        await self.send(text_data=json.dumps({
            'rps_room_name' : self.rps_room_name,
        }))

    async def disconnect(self, close_code):
        if self.rps_room_name:
            if self.rps_room_name in available_rooms:
                available_rooms.remove(self.rps_room_name)
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
                    "username" : username,
                    "rps_room_name" : self.rps_room_name
                },
            )

        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    
    async def rps_move(self, event):
        user_option = event["user_option"]
        username = event["username"]

        self.room_state.setdefault('rps_options', {})

        self.room_state['rps_options'].setdefault(username, {
            "user_option": user_option,
            "outcome_of_attempt": "",
            "outcome_of_round" : "",
            "total_wins": 0
        })
        self.room_state['rps_options'][username]["user_option"] = user_option

        self.room_state.setdefault('attempts', 3)

        if len(self.room_state['rps_options']) == 2:
            
            user1_name, user2_name = list(self.room_state['rps_options'].keys())

            user1_choice = self.room_state['rps_options'][user1_name]['user_option']
            user2_choice = self.room_state['rps_options'][user2_name]['user_option']

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
                        self.room_state['rps_options'][user1_name]['total_wins'] += 1
                        self.attempts -= 1 # only reduce the number of attempts left if either user won
                    elif rps_outcome_user_2 == "win":
                        self.room_state['rps_options'][user2_name]['total_wins'] += 1
                        self.attempts -= 1
                    
                    if self.attempts == 0:
                        if self.room_state['rps_options'][user1_name]['total_wins'] > self.room_state['rps_options'][user2_name]['total_wins']:
                            self.room_state['rps_options'][user1_name]["outcome_of_round"] = "Game Over! You won this round! You have received 10 points!"
                            self.room_state['rps_options'][user2_name]["outcome_of_round"] = "Game Over! You failed to win this game! Good luck next time!"
                            
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
                            
                        elif self.room_state['rps_options'][user2_name]['total_wins'] > self.room_state['rps_options'][user1_name]['total_wins']:
                            self.room_state['rps_options'][user1_name]["outcome_of_round"] = "Game Over! You failed to win this game! Good luck next time!"
                            self.room_state['rps_options'][user2_name]["outcome_of_round"] = "Game Over! You won this round! You have received 10 points!"

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
                        "outcome_of_attempt": rps_outcome_user_1,
                        "outcome_of_round" : self.room_state['rps_options'][user1_name]["outcome_of_round"],
                        "total_wins" : self.room_state['rps_options'][user1_name]['total_wins']
                    }

                    self.room_state['rps_options'][user2_name] = {
                        "user_option" : user2_choice,
                        "outcome_of_attempt": rps_outcome_user_2,
                        "outcome_of_round" : self.room_state['rps_options'][user2_name]["outcome_of_round"],
                        "total_wins" : self.room_state['rps_options'][user2_name]['total_wins']
                    }

                    print(self.room_state['rps_options'][user1_name])

                    await self.send(
                        text_data=json.dumps(
                            {
                                "user_list" : [user1_name, user2_name],
                                "rps_options": self.room_state['rps_options'],
                                "attempts" : self.attempts,
                                "rps_room_name" : self.rps_room_name
                            }
                        )
                    )

                    self.room_state['rps_options'][user1_name]["user_option"] = ""
                    self.room_state['rps_options'][user2_name]["user_option"] = ""
                    
                    self.room_state['rps_options'][user1_name]["outcome_of_attempt"] = ""
                    self.room_state['rps_options'][user2_name]["outcome_of_attempt"] = ""