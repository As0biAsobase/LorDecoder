  

# Lor Decoder
This is a chat bot for the social network VK and the Russian community of the Legends of Runeterra card game in it.

The bot was mainatined and developed for the purpose of helping the community discuss the game in a way that is convinient and simple. It started as a simple deck code decoding bot (hence the name) and was later updated to include new functionality.

## Deck Codes

In Legends of Runeterra, players can assemble decks of cards using in-game client and share those decks using deck codes. A deck code encodes information about cards in the deck and their quantities and can look something like this: `CECQCAICBQAQEBADAEBQIEQDAMBAECQRAYAQIAIMBUTSQLICAEAQIHABAQCBAAA`.
These codes are easy to share in group chats when discussing the game, but players have to put them inside the game or dedicated online tools to actualy know which deck is being discussed. Which is why I decided to create a bot that allowed users to turn deck codes into images without leaving group chats. 
The bot would turn a code into a more useful image:
![enter image description here](https://sun9-32.userapi.com/impg/HLx5R7-oemUVHQIOcEi640G6yr8q2UB7-anBZQ/qmklb4fZImM.jpg?size=1651x1050&quality=96&sign=47acdf23eac3734ff47869771e11b3c3&type=album)
## Card search
As the bot evolved, `cardsearch.py` module was added to allow users to search and retreive specific cards. They would simply need to tag the bot, mentioning the name of the card and bot would post the corresponding image.

## Quizes
The bot also has the `card_guesser.py` module, which would allow users to participate in automatically generated quizes - bot would retreive a random card and ask user to guess it based on the portion of its description or modified image.

## Poster
As the final adition to the bot, `poster.py` module was created that would generate daily "meta reports" - posts with information about winning decks, best-performing combinations and players, etc.
These reports were accompanied by automatically generated images, such as (shows winrates of different in-game regions combinations): 
![Winrates of region combinations](https://sun9-36.userapi.com/impg/4HIqe075UH4F9mbicgEkwJg4Z0DWcj09fgeYlQ/JA0qVO9lr2E.jpg?size=2560x1607&quality=96&sign=7e3a625a4697c734633dbec686c41046&type=album)

## Utils
The Legends of Runeterra card game had frequent upgrades and changes, so utility scripts had to be run each time this happened - these scripts would retreive new card data, regenerate card images, update MongoDB etc. These scripts are contained within the utils directory.