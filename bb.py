#!/usr/bin/env python3
import configparser
import os.path
import logging
import praw
from feedparser import parse
from time import sleep

# Set filename for logging
logging.basicConfig(filename='rss-bot.log',
                    encoding='utf-8',
                    format='%(asctime)s, %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

# Record start-up to see restarts
logging.info("\n  RSS bot started")

# Check if the config file exists
config_file = os.path.exists("config.txt")
if config_file:
  parser = configparser.ConfigParser()
  parser.read("config.txt")
else:
  logging.critical("The required config.txt doesn't exist. Please edit and rename the example_config.txt")
  exit(1)

# Parse the RSS feed for the first time, we will compare with the got entry later
last_entries_ids = []
feed_link = parser.get("config", "feed_link")
feed = parse(feed_link)
for entry in feed.entries:
  last_entries_ids.append(entry.id)
message = "Last entries' IDs at startup are: %s"
logging.info(message % last_entries_ids)

# Configure the fields to connect to Reddit
client_id = parser.get("config", "client_id")
client_secret = parser.get("config", "client_secret")
username = parser.get("config", "username")
password = parser.get("config", "password")
subreddit = parser.get("config", "subreddit").lower()
flair_id = parser.get("config", "flair_id")
reddit = praw.Reddit(user_agent="RSS-bot:v1 (by u/ItsMeRPeter)", client_id=client_id,
                     client_secret=client_secret, username=username, password=password)
reddit.validate_on_submit = True

# Endless loop what will check the RSS feed in every 10 minutes and compare if there is a new entry
# The entries' link is the unique identifier what is compared because that must be unique
while True:
  sleep(600)
  new_entry = feed.entries[0]
  new_entry_id = new_entry.id
  if new_entry_id not in last_entries_ids:
    logging.info("New article found! ID: ", new_entry_id)
# Let's check if the article is already posted in the last week
# If it's a new entry, it shouldn't be
    for submission in reddit.subreddit(subreddit).search(new_entry.title, syntax="plain", time_filter="week"):
      logging.info("The article is already posted in the subreddit. Appending it to last entries' list.")
      last_entries_ids.append(new_entry_id)
      message = "List of last entries after appending the article: %s"
      logging.info(message % last_entries_ids)
    else:
# Let's post on Reddit
      logging.info("The article wasn't shared in ", subreddit, ", let's do it now.")
      title = new_entry.title
      link = new_entry.link
      reddit.subreddit(subreddit).submit(flair_id=flair_id, title=title, url=link, send_replies=False)
      last_entries_ids.append(new_entry_id)
      logging.info("The article's ID was appeded to the last entries' list.")