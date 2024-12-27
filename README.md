# GameHive
GameHive is a Web application which allows users to play the game of their choice.

![Screenshot 2024-12-27 155048](https://github.com/user-attachments/assets/e9590ff4-f489-429e-a819-e073982fe777)


There are two games that the user can play:
1. Guess the Digit

 ![image](https://github.com/user-attachments/assets/e1f3017f-5751-4f53-8066-5ae6aee69097)
  
2. Rock, Paper, Scissors (Single Player & Multiplayer Mode)
![image](https://github.com/user-attachments/assets/e3bab2ab-13b9-4a4e-b3f7-1d3455d09aa7)


**Core Functionality:**
1. Registration - Used forms.py to create a registration form using the Django forms import. This will provide a safer authentication process.
![image](https://github.com/user-attachments/assets/72674299-a3aa-4172-b2a7-ac88197959cc)

2. Login
![image](https://github.com/user-attachments/assets/9b93aedf-d8de-4a49-bb28-f4e077d9c41c)

3. Logout

4. Profile - User can view the leaderboard and update their personal details (E.g. their password and their email)
![image](https://github.com/user-attachments/assets/e4350c7f-10f7-404e-9100-b14af3a5dbe4)

5. Testimonials - People can submit their review regarding GameHive.
![image](https://github.com/user-attachments/assets/0ed6a5cc-bd58-42bf-87bb-6e92d37b371f)

6. Two Games - User can choose between two games: Guess the Digit & Rock, Paper, Scissors.

**Core Functionality of Guessing Game:**

1. Level - User can choose between three levels: Easy, Medium, and Hard. 

2. Enable Hints - User can choose to enable or disable hints. If hints are enabled, a 50% penalty will be imposed on the points
won during that round (e.g. if user chooses easy level and they guess the correct number, but the hints are enabled, they will only
get 5 points (instead of 10 points) due to the fact that they enabled hints)

3. Number Range - Depending on the level, the user will have to guess the correct number. This is the range of numbers for each level:
(a) Easy Level - Between 1-10
(b) Medium Level - Between 1-50
(c) Hard Level - Between 1-100

4. Points - If the user guesses the correct number, they will receive points. These are the points based on the levels:
(a) Easy Level - 10 points - 5 points if the hints are enabled
(b) Medium Level - 50 points - 25 points if the hints are enabled
(c) Hard Level - 100 points - 75 points if the hints are enabled

5. Attempts - The user will be given a number of attempts to guess the correct digit, depending on the level chosen and whether they
enabled the hints for that game. This is a breakdown of the number of attempts given:
(a) Easy Level - 4 attempts if hints are DISABLED - 2 attempts if hints are ENABLED
(b) Medium Level - 10 attempts if hints are DISABLED - 5 attempts if hints are ENABLED
(c) Hard Level - 20 attempts if hints are DISABLED - 11 attempts if hints are ENABLED

**Core Functionality of Rock, Paper, Scissors**

SINGLE PLAYER MODE:

1. Player Choice - User chooses between rock, paper, scissors

2. Computer Choice - A random choice will be made between rock, paper, scissors

3. Attempts - User is given three attempts to win the round. In order to win points, they need to either:
(a) Win 3 times
(b) Win 2 times

4. Points - If the user wins the round, they will receive 10 points. This will be added to their total score for this game and the 
leaderboard for this game can be found in the profile page under the sidebar heading "Leaderboard"

MULTIPLAYER MODE:

1. Player 1 Choice - Player 1 chooses between rock, paper, scissors

2. Player 2 Choice - Player 2 chooses between rock, paper, scissors

3. Attempts - There are three attempts. In order for a player to win, they must get either:
(a) Win 3 times
(b) Win 2 times

4. Points - If one of the players win the round, they will get 10 points, which will be added to the leaderboard score.

**Testing**

Testing is required with any app that is being created. For GameHive, unit testing and integration testing were/are being used to test
a variety of functionalities such as:
1. Registration process
2. Login process
3. Testimonials form
4. Update personal details form
5. Change password form

Additionally, unit & integration tests were used to test:
1. Guess the Digit game using valid and invalid inputs, as well as simulating the process using each level and hints enabled/disabled.
2. Rock, Paper, Scissors game, where there were two integration tests: A situation where the user has lost the round and a situation where the user has won the round.

This ensures that these aspects of GameHive work correctly. The test files are called tests.py and can be found in this project.
