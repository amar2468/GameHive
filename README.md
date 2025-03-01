# GameHive
GameHive is a Web application which allows users to play the game of their choice.

![image](https://github.com/user-attachments/assets/360422e1-7c84-47b6-96b0-3505c098be7e)

There are two games that the user can play:
1. Guess the Digit

 ![image](https://github.com/user-attachments/assets/7efa30f7-4710-4ada-b8c0-d96a27f5446d)

  
2. Rock, Paper, Scissors (Single Player & Multiplayer Mode)
   
![image](https://github.com/user-attachments/assets/5cded345-c3a6-4c0d-814b-26737ba34e81)

**Core Functionality:**
1. Registration - Used forms.py to create a registration form using the Django forms import. This will provide a safer authentication process.

![image](https://github.com/user-attachments/assets/98d29308-e53b-475b-8771-5340b163ca93)


2. Login

![image](https://github.com/user-attachments/assets/afc1f39b-741b-4036-8d3d-6852275cb465)


3. Logout

4. Profile - User can view the leaderboard and update their personal details (E.g. their password and their email)

![image](https://github.com/user-attachments/assets/4a877e29-b0eb-4770-b4aa-46b25b1f22c8)

5. Testimonials - People can submit their review regarding GameHive.

![image](https://github.com/user-attachments/assets/18064162-6fd2-46b7-8670-57e8e73a93e5)


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
