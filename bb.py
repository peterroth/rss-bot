#!/usr/bin/env python3
import configparser
import feedparser
import os.path
import praw
import time

# Check if the config file exists
config_file = os.path.exists("config.txt")
if config_file:
    parser = configparser.ConfigParser()
    parser.read("config.txt")
else:
    print("The required config.txt doesn't exist. Please edit and rename the example_config.txt")
    exit(1)

# Parse the RSS feed for the first time, we will compare with the got entry later
feed_link = parser.get("config", "feed_link")
feed = feedparser.parse(feed_link)
last_entry = feed.entries[0]
last_entry_link = last_entry.link

# Configure the fields to connect to Reddit
client_id = parser.get("config", "client_id")
client_secret = parser.get("config", "client_secret")
username = parser.get("config", "username")
password = parser.get("config", "password")
subreddit = parser.get("config", "subreddit")
flair_id = parser.get("config", "flair_id")
reddit = praw.Reddit(user_agent="GCP:Blog-bot:v1 (by u/ItsMeRPeter)", client_id=client_id,
                     client_secret=client_secret, username=username, password=password)
reddit.validate_on_submit = True

# Endless loop what will check the RSS feed in every 10 minutes and compare if there is a new entry
# The entries' link is the unique identifier what is compared because that must be unique
while True:
    time.sleep(600)
    feed = feedparser.parse(feed_link)
    new_entry = feed.entries[0]
    new_entry_link = new_entry.link
    if new_entry_link != last_entry_link:
        title = new_entry.title
        link = new_entry_link
# Let's post on Reddit
        reddit.subreddit(subreddit).submit(flair_id=flair_id, title=title, url=link, send_replies=False)
        last_entry_link = new_entry_link
