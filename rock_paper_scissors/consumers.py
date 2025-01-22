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
                    "username" : username
                },
            )

        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    
    async def rps_move(self, event):
        # Extracting the rps option (rock,paper, or scissors) & username from client-side.
        user_option = event["user_option"]
        username = event["username"]

        # If "rps_options" dictionary (which holds the rps option, outcome of round, and outcome of game for each user) doesn't exist,
        # it will create an empty dictionary. Otherwise, it will move to the next block of code.
        self.room_state.setdefault('rps_options', {})

        # As in the case above, if the current user does not have a record in rps_options, it will populate it with the info below.
        self.room_state['rps_options'].setdefault(username, {
            "user_option": user_option,
            "outcome_of_round": "",
            "outcome_of_game" : "",
            "total_wins": 0
        })

        # Storing the variable that stores the rps choice from the user in the rps_options dictionary.
        self.room_state['rps_options'][username]["user_option"] = user_option

        # Setting the attempts to 3. The attempts will only be decremented, if either user wins.
        self.room_state.setdefault('attempts', 3)

        # If two users have made a move (chosen between rock,paper,scissors), this "if" statement will be executed.
        if len(self.room_state['rps_options']) == 2:
            
            # From the "rps_options" dictionary, we are extracting the usernames of the two users
            user1_name, user2_name = list(self.room_state['rps_options'].keys())

            # Storing both user choices in variables, so that they can be used in the "if" statement below
            user1_choice = self.room_state['rps_options'][user1_name]['user_option']
            user2_choice = self.room_state['rps_options'][user2_name]['user_option']

            # If both users made a move, it will start to compare their choices and decide the outcome of the round or game.
            if user1_choice != "" and user2_choice != "":
                
                # If we have not run out of attempts, we can then compare the user choices
                if self.attempts > 0:

                    # Created a dictionary which will identify what the outcome of a round should be, relative to the user choice
                    rps_outcomes = {
                        'rock' : {'paper' : 'lose', 'scissors' : 'win'},
                        'paper' : {'rock' : 'win', 'scissors' : 'lose'},
                        'scissors' : {'rock' : 'lose', 'paper' : 'win'}
                    }

                    # Here, we are comparing the choices of the users. It will result in either "win", "lose", or "draw"
                    rps_outcome_user_1 = rps_outcomes[user1_choice].get(user2_choice, 'draw')
                    rps_outcome_user_2 = rps_outcomes[user2_choice].get(user1_choice, 'draw')

                    # In the if..elif block below, we are checking whether either user "won" the round. If so, their total win record
                    # will be incremented and the number of attempts left for both users will reduce by 1
                    if rps_outcome_user_1 == "win":
                        self.room_state['rps_options'][user1_name]['total_wins'] += 1
                        self.attempts -= 1 # only reduce the number of attempts left if either user won
                    elif rps_outcome_user_2 == "win":
                        self.room_state['rps_options'][user2_name]['total_wins'] += 1
                        self.attempts -= 1
                    
                    # If we have no attempts left, then we know that we have a winner.
                    if self.attempts == 0:
                        # If any user won, the user that won will get a message indicating that they won the game, while the user that
                        # lost will get a message that they lost the game.
                        if self.room_state['rps_options'][user1_name]['total_wins'] > self.room_state['rps_options'][user2_name]['total_wins']:
                            self.room_state['rps_options'][user1_name]["outcome_of_game"] = "Game Over! You won this game! You have received 10 points!"
                            self.room_state['rps_options'][user2_name]["outcome_of_game"] = "Game Over! You failed to win this game! Good luck next time!"
                            
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
                            self.room_state['rps_options'][user1_name]["outcome_of_game"] = "Game Over! You failed to win this game! Good luck next time!"
                            self.room_state['rps_options'][user2_name]["outcome_of_game"] = "Game Over! You won this game! You have received 10 points!"

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
                        "outcome_of_round": rps_outcome_user_1,
                        "outcome_of_game" : self.room_state['rps_options'][user1_name]["outcome_of_game"],
                        "total_wins" : self.room_state['rps_options'][user1_name]['total_wins']
                    }

                    self.room_state['rps_options'][user2_name] = {
                        "user_option" : user2_choice,
                        "outcome_of_round": rps_outcome_user_2,
                        "outcome_of_game" : self.room_state['rps_options'][user2_name]["outcome_of_game"],
                        "total_wins" : self.room_state['rps_options'][user2_name]['total_wins']
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

                    self.room_state['rps_options'][user1_name]["user_option"] = ""
                    self.room_state['rps_options'][user2_name]["user_option"] = ""
                    
                    self.room_state['rps_options'][user1_name]["outcome_of_round"] = ""
                    self.room_state['rps_options'][user2_name]["outcome_of_round"] = ""