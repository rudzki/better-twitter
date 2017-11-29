from twitter import *
import re
import mechanicalsoup

# constants set in external creds.py file

from creds import TWITTER_KEY, TWITTER_KEY_SECRET, TWITTER_TOKEN, TWITTER_TOKEN_SECRET

# credentials

config = {
    "consumer_key" : TWITTER_KEY,
    "consumer_secret" : TWITTER_KEY_SECRET,
    "access_key" : TWITTER_TOKEN,
    "access_secret" : TWITTER_TOKEN_SECRET
}

# twitter api object

twitter = Twitter(
    auth = OAuth(config["access_key"],
    config["access_secret"],
    config["consumer_key"],
    config["consumer_secret"]),
    secure=True)
results = twitter.statuses.home_timeline()

# 1. iterate over tweets, find links outside twitter.com
# 2. remove trailing query strings from URLs
# 3. fetch page name from URL

for tweet in results:
    for url in tweet["entities"]["urls"]:
        if ( "https://twitter.com" not in url["expanded_url"] ):
            tweet_username = tweet["user"]["screen_name"]
            tweet_url = re.sub('\?.*', '', url["expanded_url"])
            browser = mechanicalsoup.StatefulBrowser()
            browser.open(tweet_url)
            page = browser.get_current_page()
            tweet_title = page.title.text
            print(tweet_title + " " + "[@" + tweet_username + "]",
                  "\n", tweet_url, "\n")


# todo: returned tweets seem few; probably hitting limit
# todo: store in database for X days
# todo: web interface using flask

