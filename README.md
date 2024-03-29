# WHAT  
RSS bot is a simple Python script to parse an RSS feed and if a new post is noticed post its title and URL in a given subreddit on Reddit.  
My original idea was to follow a blog and post new content in a subreddit, but the bot can be used with any RSS feed (news, blog, tech, anything).  
  
# HOW  
Install the required Python packages with *pip*:  
`pip install -r requirements.txt`  
Copy and rename the `example_config.txt` to `config.txt`. Edit the fields within the file.  
The first section's name must remain DEFAULT, the other two can be changed, and you can add additional sections, the script will iterate over them continuously to parse the RSS feed.  
To get the client ID and secret you must visit the [Apps page on Reddit](https://ssl.reddit.com/prefs/apps/), create a new application with "Script" type.  
After the config file is filled with the required data you can start the script. To keep it running in the background use *nohup*:  
`nohup python3 rss.py &`  
The default delay between 2 RSS fetches is 10 minutes.  
  
# CONTRIBUTE  
Feel free to clone the repo, edit the script and create Pull Requests. I'm open for optimisations, new features, fixes, etc.