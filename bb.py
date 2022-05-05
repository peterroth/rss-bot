# Blog-bot that parses an RSS and if a new entry is shown posts its title and URL in a subreddit
import configparser
import feedparser
import os.path
import praw
import time

config_file = os.path.exists("config.txt")
if config_file:
    parser = configparser.ConfigParser()
    parser.read("config.txt")
else:
    print("The required config.txt doesn't exist. Please edit and rename the example_config.txt")
    exit(1)

feed_link = parser.get("config", "feed_link")
feed = feedparser.parse(feed_link)
last_entry = feed.entries[0]
last_entry_link = last_entry.link

client_id = parser.get("config", "client_id")
client_secret = parser.get("config", "client_secret")
username = parser.get("config", "username")
password = parser.get("config", "password")
subreddit = parser.get("config", "subreddit")
flair_id = parser.get("config", "flair_id")
reddit = praw.Reddit(user_agent="GCP:Blog-bot:v1 (by u/ItsMeRPeter)", client_id=client_id,
                     client_secret=client_secret, username=username, password=password)
reddit.validate_on_submit = True

while True:
    time.sleep(600)
    feed = feedparser.parse(feed_link)
    new_entry = feed.entries[0]
    new_entry_link = new_entry.link
    if new_entry_link != last_entry_link:
        title = new_entry.title
        link = new_entry_link
        reddit.subreddit(subreddit).submit(flair_id=flair_id, title=title, url=link, send_replies=False)
        last_entry_link = new_entry_link
