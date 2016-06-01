# kingdom_bot

A reddit bot which would run a partially text-based risk-style game over reddit.  

[**Partially outdated design document**](https://docs.google.com/document/d/1f14WI7LXzqelAXwRaoX8AQeXkZnzHfj1ZVnSahfWVds/edit?usp=sharing)

To run it you'll need your own obot.py file, which would have the proper credentials needed to access your reddit account.  To make one, [**follow the tutorial here.**](https://www.reddit.com/r/GoldTesting/comments/3cm1p8/how_to_make_your_bot_use_oauth2/)

The test subreddit I'm using is [**/r/TheFifthHorse**](https://www.reddit.com/r/TheFifthHorse/)

You can see the [**maps**](https://www.reddit.com/r/TheFifthHorse/wiki/index) and [**player list**](https://www.reddit.com/r/TheFifthHorse/wiki/players) in their respective wiki pages.  

The bot would need mod access to the subreddit in order to update the maps, so I recommend changing the target subreddit to do your own testing.  

# What does it do?

`reddit_bot.py` runs the to-and-for with reddit.  It loads or creates a map using **counties_maker_2.py**, and then every thirty seconds it:

* Processes requests from users summoning it
* Updates the game maps
* Uploads the game maps to the subreddit wiki
* Pays the rulers proportional to the number of counties they own and the productivity of those counties
* Saves the game state using pickle

`counties_maker_2.py` is imported by **reddit_bot.py**, and holds the class definitions for the data structures which represent holdings, kingdoms, and rulers.  It also creates a map of different counties that users can take control of.  

`kingdoms_test.py` is a side-project not yet integrated into the game.  It is a more realistic, procedurally generated map, which ideally would be used to generate productivity values for the different counties depending on the biome.  

#Map generation

The map created by `counties_maker_2.py` is represented by a 256*256 pixel grid, divided in between 200 different counties.  

Here's how the algorithm works:

* Randomly pick 200 points within the empty map.  These "capitals" are essentially each county's starting point.  
* Iterate the following until all squares are claimed:
  * For every county, do the following:
   * Get edge_territory, a list of all squares on the exterior of the county (the capital is automatically placed in this list)
   * For every square in edge_territory, add the adjacent squares not already claimed by a county to a list called adjacent
    * If there are no unclaimed adjacent squares, remove the square from edge_territory (as obviously its no longer on the edge)
   * Pick a random square from adjacent and add it to the county's territory

This method allows the counties to have semi-realistic borders with each-other.  

![Looks a bit like a bacteria culture, doesn't it?](https://i.imgur.com/b6HcSyJ.gif)

It also produces a nice-looking gif (this one was made by outputting the map every ten steps, so for every frame, each territory will gain 10 additional squares, unless it has been blocked in by its neighbors already.)

The mad race for territory when there's only one direction to expand is interesting, but the long smears of territory are not really ideal when trying to emulate real-world political borders.  This could likely be improved by use of [Lloyd's algorithm](https://en.wikipedia.org/wiki/Lloyd%27s_algorithm) to fight off [clustering](https://en.wikipedia.org/wiki/Clustering_illusion) a little bit.  (See also [here](http://bit-player.org/2011/a-slight-discrepancy))

