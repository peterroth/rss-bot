#!/usr/bin/env python3
import configparser
import logging
import praw
from feedparser import parse
from os import path
from time import sleep

# Set filename for logging
logging.basicConfig(filename='rss-bot.log',
                    encoding='utf-8',
                    format='%(asctime)s, %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

# Record start-up to see restarts
logging.info("RSS bot started")

# Check if the config file exists
if path.exists("config.txt"):
  config = configparser.ConfigParser()
  config.read("config.txt")
else:
  logging.critical("The required config.txt doesn't exist. Please edit and rename the example_config.txt")
  exit(1)

# Parse the RSS feed for the first time, we will compare with the got entry later
last_entries_ids = []
for section in config.sections():
  feed_link = config.get(section, "feed_link")
  feed = parse(feed_link)
  for entry in feed.entries:
    last_entries_ids.append(entry.id)
message = "Last entries' IDs at startup are: %s"
logging.debug(message % last_entries_ids)

# Configure the fields to connect to Reddit
user = config['DEFAULT']
client_id = user['client_id']
client_secret = user['client_secret']
username = user['username']
password = user['password']
reddit = praw.Reddit(user_agent="RSS-bot:v2 (by u/ItsMeRPeter)",
                     client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password)

# Endless loop what will check the RSS feed in every 10 minutes and compare if there is a new entry
# The entries' link is the unique identifier what is compared because that must be unique
while True:
  sleep(600)
  for section in config.sections():
    try:
      feed = parse(config.get(section, "feed_link"))
    except Exception as e:
      logging.error(f"Couldn't parse the RSS feed, the error was: {e}")
      continue
    new_entry = feed.entries[0]
    new_entry_id = new_entry.id
    if new_entry_id not in last_entries_ids:
      message = "New article found! ID: %s"
      logging.info(message % new_entry_id)
  # Let's check if the article is already posted in the last week
  # If it's a new entry, it shouldn't be
      subreddit = config.get(section, "subreddit")
      for submission in reddit.subreddit(subreddit).search(new_entry.title, syntax="plain", time_filter="week"):
        logging.info("The article is already posted in " + subreddit.upper() + "; it'll be appended to last entries' list")
        last_entries_ids.append(new_entry_id)
        message = "List of last entries after appending the article: %s"
        logging.debug(message % last_entries_ids)
      else:
  # Let's post on Reddit
        logging.info("The article wasn't shared in " + subreddit.upper() + " yet, let's do it now.")
        flair_id = config.get(section, "flair_id")
        try:
          reddit.subreddit(subreddit).submit(flair_id=flair_id, title=new_entry.title, url=new_entry.link, send_replies=False)
        except Exception as e:
          logging.error("Posting in " + subreddit.upper() + f" wasn't successful: {e}")
          continue
        else:
          logging.info("Article successfully posted in " + subreddit.upper() + "! Everything is good.")
          last_entries_ids.append(new_entry_id)
          logging.debug("The article's ID was appeded to the last entries' list.")