# kingdom_bot

A reddit bot which would run a partially text-based risk-style game over reddit.  

[**Partially outdated design document**](https://docs.google.com/document/d/1f14WI7LXzqelAXwRaoX8AQeXkZnzHfj1ZVnSahfWVds/edit?usp=sharing)

To run it you'll need your own obot.py file, which would have the proper credentials needed to access your reddit account.  To make one, [**follow the tutorial here.**](https://www.reddit.com/r/GoldTesting/comments/3cm1p8/how_to_make_your_bot_use_oauth2/)

The test subreddit I'm using is [**/r/TheFifthHorse**](https://www.reddit.com/r/TheFifthHorse/)

You can see the [**maps**](https://www.reddit.com/r/TheFifthHorse/wiki/index) and [**player list**](https://www.reddit.com/r/TheFifthHorse/wiki/players) in their respective wiki pages.  

The bot would need mod access to the subreddit in order to update the maps, so I recommend changing the target subreddit to do your own testing.  

# What does it do?

**reddit_bot.py** runs the to-and-for with reddit.  It loads or creates a map using **counties_maker_2.py**, and then every thirty seconds it:

* Processes requests from users summoning it
* Updates the game maps
* Uploads the game maps to the subreddit wiki
* Pays the rulers proportional to the number of counties they own and the productivity of those counties
* Saves the game state using pickle

**counties_maker_2.py**

This file is imported by **reddit_bot.py**, and holds the class definitions for the data structures which represent holdings, kingdoms, and rulers.  It also creates a map of different counties that users can take control of.  

The map is represented by a 256*256 pixel grid, divided in between 200 different counties.  

##Map generation

![Looks a bit like a bacteria culture, doesn't it?](https://i.imgur.com/b6HcSyJ.gif)
