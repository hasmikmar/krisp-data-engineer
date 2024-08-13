############
#
# Extract Titles from RSS feed
#
# Implement get_headlines() function. It should take a url of an RSS feed
# and return a list of strings representing article titles.
#
############

# pip install feedparser 
import feedparser

google_news_url = "https://news.google.com/rss"

def get_headlines(rss_url):
    feed = feedparser.parse(rss_url)
    return [key.title for key in feed['entries']]

print(get_headlines(google_news_url))