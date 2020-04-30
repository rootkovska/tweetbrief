import datetime
import logging
import os
from collections import namedtuple
from heapq import nlargest
from pprint import pprint

import tweepy

Tweet = namedtuple("Tweet", "author text")


class TwitterExtractor:
    def __init__(self, consumer_key, consumer_secret):
        self.logger = logging.getLogger(__name__)
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def extract_tweets(self, username, single_author_max_tweets, period):
        self.logger.info("Searching for a user...")
        user = self.api.get_user(username)

        self.logger.info("Loading user's friends...")
        friends = tweepy.Cursor(self.api.friends, user_id=user.id).items()

        since = datetime.datetime.now() - datetime.timedelta(days=period)
        since = since.strftime("%Y-%m-%d")

        tweets = []
        for friend in friends:
            friend_top_tweets = self.__get_top_tweets(friend.screen_name, single_author_max_tweets, since)
            for tweet in friend_top_tweets:
                tweets.append(Tweet(tweet.user.screen_name, tweet.text))

        return tweets

    def __get_top_tweets(self, username, tweets_num, since):
        query = f"from:{username} since:{since} -filter:retweets"
        tweets = tweepy.Cursor(self.api.search, q=query).items()

        return nlargest(tweets_num, tweets, key=lambda tweet: tweet.retweet_count)
