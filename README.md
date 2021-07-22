# Tribalwars Bot
This app is a farming bot for the tribal wars game. The bot is easily configurable and provides flexibility in this configuration. If an error occurs or a capcha appears, the bot notifies the user of this event by sending an email. All you have to do is configure it once and run the program. All available options are listed and explained below.

"Username" - your Tribal Wars username
"Password" - your Tribal Wars password
"Email" - your email address (used as sender and receiver)
"EmailPassword" - password to your email address (required to send notifications)
"Premium" - 0 means no Premium, 1 means Premium
"NumVillages" - number of villages from which you wish to farm
"CustomAttack" - 1 if you want to send farms attacks to custom cords (for example other inactive players), 0 if you wont. If you choose 1, provide cords in Cords.txt file
"NoFarm" - list of villages you want to exlude from farming. Notation like this: [1,5,6]
"APatternAttacs" - if you want to send other patterns than LC, specify here how many of these attacks you want to send
"Pattern" - if mode == 1, specify how many attacks you want to send, from each village.
"Pages" - how many farm pages you wish to use (how far to send farm)
"Mode" - just pass 1
"Split" - how much to divide the maximum number of available units 
"World" - world number

Sample Options file available in project

# Instalation
1. Install python 3.6
2. Run "pipenv shell"
3. Run "pipenv install"
4. Provide required data in Options.json
