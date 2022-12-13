# League-of-TFT

This web application is designed to be used by players of the video game "Teamfight Tactics" (also referred to as TFT). It allows a player to input specific parameters in order to view advanced stats from their game history from recent TFT games. These statistics are not available to a player within the game client, so some of these insights may be useful for improving your gameplay, or to simply compare statistics with your friends from recent games.

Instructions:
1) Download dependencies and load async server using uvicorn: uvicorn app:app --reload
2) Launch browser at provided route (copy and paste terminal link in browser, e.g. http://127.0.0.1:8000)
3) Retrieve your Riot API Key from the Riot Games Developer Portal at https://developer.riotgames.com/ - Note: You will need to login with a valid riot account to retrieve an API Key. Additionally, your API Key will need to be regenerated every 24 hours.
4) Enter inputs for Match Count, Region, Summoner Name, and API Key. Click "Submit and Generate Summary Statistics". With a proper entry, you will be redirected to a page that details your advanced statistics such as Average Damage, Average Placement, Average Players Eliminated, and Average Final Level.
5) To include different summoners or other criteria for comparison, refresh the url and make another entry.




Upcoming Changes:
1) To host application online, to make it available for TFT players to use on the web.
2) To visualize data for all summoners using an interactive graph that allows for better comparisons when viewing multiple summoners.
3) To work on speeding up app response time when making calls to the Riot API.
4) To include additional summary statistics after determining which metrics are relevant enough to add.
