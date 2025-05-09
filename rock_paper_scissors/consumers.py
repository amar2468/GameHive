from channels.generic.websocket import AsyncWebsocketConsumer
import json
from gamehive.models import GameUserProfile, CustomUser
from asgiref.sync import sync_to_async
import random
import redis
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

# We are retrieving the redis URL from the .env file, so that we can extract the hostname, password, and port number, which are
# all needed for the part where we connect to the Redis instance.
load_dotenv()

redis_url = os.getenv("REDIS_URL")

url = urlparse(redis_url)

# Creating an instance of the Redis client
redis_client = redis.Redis(host=url.hostname, password=url.password, port=url.port, ssl=True, decode_responses=True)

class RockPaperScissorsConsumer(AsyncWebsocketConsumer):
    # Creating a constant variable that stores the total number of wins required to win the game
    WINS_REQUIRED_TO_WIN = 3

    # This variable will be used when checking if both users have joined the session
    REQUIRED_NUMBER_OF_USERS = 2

    async def connect(self):
        # We are retrieving the current user who has just connected to the multiplayer rock,paper,scissors game
        current_user = self.scope['user']

        # Retrieving the rooms - specifically which ones have been populated by 1 user. If there are no rooms that are currently
        # populated, it will return an empty list
        available_rooms = redis_client.lrange("available_rooms", 0, -1) or []

        # Retrieving the users and what room they are located in. Returns an empty dictionary if users are not present in any room.
        users_in_session = redis_client.hgetall("users_in_session") or {}

        # If there are no players in any room, then generate a random room for the user to enter in.
        if not available_rooms:
            rps_room_name = random.randint(1,100)

            rps_room_name = str(rps_room_name)

            self.rps_room_name = rps_room_name

            # Using the Redis client, we are adding the room number to the list of rooms that can be populated by another user
            redis_client.rpush("available_rooms", self.rps_room_name)

            # Adding the first user to the users_in_session dictionary. The key will be the room number, while the value is the 
            # users in it
            current_users_in_session = [current_user.username]

            # Using Redis client, we are adding the current user to the users_in_session dictionary, with the room number as the key
            redis_client.hset("users_in_session", self.rps_room_name, json.dumps(current_users_in_session))
        
        # If there are available rooms (Rooms that have one player waiting), add the user to the first available one.
        else:
            # We can remove the room from the list of available rooms, as it will be populated by another user - (2 players per room)
            self.rps_room_name = redis_client.lpop("available_rooms")

            # Retrieving the users_in_session dictionary, so that we can append the second user to the "value" part of the "key", which
            # is the room number.
            current_users_in_session = redis_client.hget("users_in_session", self.rps_room_name)

            # We need to retrieve the current user in the room and convert the result into a list. This will allow us to append the
            # second user to the list and then return the result.
            if current_users_in_session:
                current_users_in_session = json.loads(current_users_in_session)

            # Appending the second user to the list
            current_users_in_session.append(current_user.username)

            # Updating the Redis client with the two users that have joined the specific room number
            redis_client.hset("users_in_session", self.rps_room_name, json.dumps(current_users_in_session))

        self.room_state = {}

        await self.channel_layer.group_add(self.rps_room_name, self.channel_name)

        await self.accept()
        
        # Retrieve the current users that are located in a room
        current_users_session = redis_client.hget("users_in_session", self.rps_room_name)

        # If there is at least one user who is in the specific room, retrieve the users that are populated in that room
        if current_users_session:
            current_users_session = json.loads(current_users_session)
        # If no one is in the room, just create an empty list to show this
        else:
            current_users_session = []

        # Count how many users are in the current room
        number_of_users_in_session = len(current_users_session)

        # If two people are in the mentioned room, we will inform the client side that both users are in the room and the game can commence.
        if number_of_users_in_session == RockPaperScissorsConsumer.REQUIRED_NUMBER_OF_USERS:
            await self.channel_layer.group_send(
                self.rps_room_name,
                {
                    'type' : 'start_rps_game',
                    'rps_room_name' : self.rps_room_name,
                }
            )
        # If the room does not have 2 users, we will just send the room name back to the client-side.
        else:
            await self.send(text_data=json.dumps({
                'rps_room_name' : self.rps_room_name,
            }))

    async def disconnect(self, close_code):
        # We are retrieving all the rooms which have been populated by at least one user. If there are no rooms like that, we represent
        # it with an empty list instead.
        available_rooms = redis_client.lrange("available_rooms", 0, -1) or []

        if self.rps_room_name:
            # If the specific room is populated by at least one user, remove the room as the session has disconnected
            if self.rps_room_name in available_rooms:
                redis_client.lrem("available_rooms", 1, self.rps_room_name)
            # If the specific room was in the dictionary that holds the room as the "key" and the users in it as the "value", we want
            # to delete this room from the dictionary, along with the users in it, as the session has disconnected.
            if redis_client.hexists("users_in_session", self.rps_room_name):
                redis_client.hdel("users_in_session", self.rps_room_name)
        print(f"WebSocket Disconnected with code: {close_code}")

        await self.channel_layer.group_send(
            self.rps_room_name,
            {
                'type' : 'end_game',
                'rps_room_name' : self.rps_room_name,
            }
        )

        await self.channel_layer.group_discard(self.rps_room_name, self.channel_name)
    
    async def start_rps_game(self, event):
        await self.send(text_data=json.dumps(
            {
                'type' : 'start_rps_game', 
                'rps_room_name' : self.rps_room_name
            }
        ))
    
    async def end_game(self, event):
        await self.send(text_data=json.dumps(
            {
                'type' : 'end_game',
                'rps_room_name' : self.rps_room_name,
            }
        ))
    
    # If one user makes a move, this event type async function will be executed, sending the event type and the username of the 
    # user who made the move.
    async def opponent_move(self, event):
        await self.send(text_data=json.dumps(
            {
                'type' : 'opponent_move',
                'rps_room_name' : self.rps_room_name,
                'opponent_username' : event['opponent_username']
            }
        ))

    async def receive(self, text_data):
        print(f"Received raw data: {text_data}")

        try:
            data = json.loads(text_data)
            username = data["username"]
            user_option = data["user_option"]
            
            await self.channel_layer.group_send(
                self.rps_room_name,
                {
                    "type" : "rps_move",
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

        # If two users have made a move (chosen between rock,paper,scissors), this "if" statement will be executed.
        if len(self.room_state['rps_options']) == 2:
            
            # From the "rps_options" dictionary, we are extracting the usernames of the two users
            user1_name, user2_name = list(self.room_state['rps_options'].keys())

            # Storing both user choices in variables, so that they can be used in the "if" statement below
            user1_choice = self.room_state['rps_options'][user1_name]['user_option']
            user2_choice = self.room_state['rps_options'][user2_name]['user_option']

            # If both users made a move, it will start to compare their choices and decide the outcome of the round or game.
            if user1_choice != "" and user2_choice != "":

                # Created a dictionary which will identify what the outcome of a round should be, relative to the user choice
                rps_outcomes = {
                    'rock' : {'paper' : 'lose', 'scissors' : 'win'},
                    'paper' : {'rock' : 'win', 'scissors' : 'lose'},
                    'scissors' : {'rock' : 'lose', 'paper' : 'win'}
                }

                # Here, we are comparing the choices of the users. It will result in either "win", "lose", or "draw"
                rps_outcome_user_1 = rps_outcomes[user1_choice].get(user2_choice, 'draw')
                rps_outcome_user_2 = rps_outcomes[user2_choice].get(user1_choice, 'draw')

                # In the if..elif block below, we are checking whether either user "won" the round. If any of them did, their "total_win"
                # record will be increased by 1
                if rps_outcome_user_1 == "win":
                    self.room_state['rps_options'][user1_name]['total_wins'] += 1
                elif rps_outcome_user_2 == "win":
                    self.room_state['rps_options'][user2_name]['total_wins'] += 1
                
                # The user that gets 3 wins first wins the game, while the user that lost will get a message that they lost the game.
                if self.room_state['rps_options'][user1_name]['total_wins'] == RockPaperScissorsConsumer.WINS_REQUIRED_TO_WIN:
                    self.room_state['rps_options'][user1_name]["outcome_of_game"] = "Game Over! You won this game! You have received 10 points!"
                    self.room_state['rps_options'][user2_name]["outcome_of_game"] = "Game Over! You failed to win this game! Good luck next time!"
                    
                    # Attempt to update the user score by 10, if they won. Except part will run if this is the user's first ever game
                    try:
                        # Retrieving the username
                        user_instance = await sync_to_async(CustomUser.objects.get)(username=user1_name)
                        # Based on the username, we are trying to find the game record that goes with the username
                        game_user_profile = await sync_to_async(GameUserProfile.objects.get)(user=user_instance)
                        # Increase the user score by 10, as they won
                        game_user_profile.current_score += 10
                        # Save the record
                        await sync_to_async(game_user_profile.save)()
                    except GameUserProfile.DoesNotExist:
                        # Retrieving the username
                        user_instance = await sync_to_async(CustomUser.objects.get)(username=user1_name)
                        # Create the user profile that will keep track of the points won. Set the score to be 10, as they won.
                        game_user_profile = await sync_to_async(GameUserProfile.objects.create) (
                            user = user_instance,
                            current_score = 10,
                        )
                
                # The user that gets 3 wins first wins the game, while the user that lost will get a message that they lost the game.
                elif self.room_state['rps_options'][user2_name]['total_wins'] == RockPaperScissorsConsumer.WINS_REQUIRED_TO_WIN:
                    self.room_state['rps_options'][user1_name]["outcome_of_game"] = "Game Over! You failed to win this game! Good luck next time!"
                    self.room_state['rps_options'][user2_name]["outcome_of_game"] = "Game Over! You won this game! You have received 10 points!"

                    # Attempt to update the user score by 10, if they won. Except part will run if this is the user's first ever game
                    try:
                        # Retrieving the username
                        user_instance_2 = await sync_to_async(CustomUser.objects.get)(username=user2_name)
                        # Based on the username, we are trying to find the game record that goes with the username
                        game_user_profile = await sync_to_async(GameUserProfile.objects.get)(user=user_instance_2)
                        # Increase the user score by 10, as they won
                        game_user_profile.current_score += 10
                        # Save the record
                        await sync_to_async(game_user_profile.save)()
                    except GameUserProfile.DoesNotExist:
                        # Retrieving the username
                        user_instance_2 = await sync_to_async(CustomUser.objects.get)(username=user2_name)
                        # Create the user profile that will keep track of the points won. Set the score to be 10, as they won.
                        game_user_profile = await sync_to_async(GameUserProfile.objects.create) (
                            user = user_instance_2,
                            current_score = 10,
                        )
                # Updating the rps_options dictionary with the latest information from the game, so that it can be sent back to client-side
                self.room_state['rps_options'][user1_name] = {
                    "user_option" : user1_choice,
                    "outcome_of_round": rps_outcome_user_1,
                    "outcome_of_game" : self.room_state['rps_options'][user1_name]["outcome_of_game"],
                    "total_wins" : self.room_state['rps_options'][user1_name]['total_wins']
                }

                # Updating the rps_options dictionary with the latest information from the game, so that it can be sent back to client-side
                self.room_state['rps_options'][user2_name] = {
                    "user_option" : user2_choice,
                    "outcome_of_round": rps_outcome_user_2,
                    "outcome_of_game" : self.room_state['rps_options'][user2_name]["outcome_of_game"],
                    "total_wins" : self.room_state['rps_options'][user2_name]['total_wins']
                }

                # Sending back the list that contains both usernames, the outcome of the round or game, and the room number.
                # This will be sent back to the client-side part. It will be sent in the form of JSON.
                await self.send(
                    text_data=json.dumps(
                        {
                            "user_list" : [user1_name, user2_name],
                            "rps_options": self.room_state['rps_options'],
                            "rps_room_name" : self.rps_room_name
                        }
                    )
                )

                # After the information is sent to the client-side, we want to clear the options that the users chose
                # This is done so that their options are not remembered in the next round, which would lead to inaccuracies in the result
                self.room_state['rps_options'][user1_name]["user_option"] = ""
                self.room_state['rps_options'][user2_name]["user_option"] = ""
                
                # After the information is sent to the client-side, we want to clear the outcome of that particular round.
                # This is done so that the outcome of the round is not remembered in the next round.
                self.room_state['rps_options'][user1_name]["outcome_of_round"] = ""
                self.room_state['rps_options'][user2_name]["outcome_of_round"] = ""
            
            # In this block, I want to see if one of the users picked their choice. If they did, we want to trigger the 
            # "opponent_move" event type. The information will be sent to the front-end, where we will change the behaviour in the
            # template (hide the loading spinner & change the text)
            elif (user1_choice == "" and user2_choice != "") or (user1_choice != "" and user2_choice == ""):

                await self.channel_layer.group_send(
                    self.rps_room_name,
                    {
                        'type' : 'opponent_move',
                        'opponent_username' : username,
                        'rps_room_name' : self.rps_room_name,
                    }
                )