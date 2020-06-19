import heapq
import logging
from datetime import datetime, timedelta
from itertools import chain
from typing import List

import tweepy

from twitterapi.simple_tweet import SimpleTweet


class TweetExtractor:
    def __init__(self, consumer_key: str, consumer_secret: str, tweet_mode: str = "compat") -> None:
        self.logger = logging.getLogger(__name__)
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.tweet_mode = tweet_mode

        if tweet_mode not in ["compat", "extended"]:
            self.logger.warning(f"Unknown tweet_mode: `{tweet_mode}! Setting to default...")
            self.tweet_mode = "compat"

    def extract_top_tweets(
        self, username: str, single_author_max_tweets: int, tweets_num: int, days_back: int
    ) -> List[SimpleTweet]:
        self.logger.info(f"Searching for `{username}`...")

        user = self.api.get_user(username)

        self.logger.info("Loading following authors...")

        authors = tweepy.Cursor(self.api.friends, user_id=user.id).items()

        tweets = chain.from_iterable(
            map(
                lambda author: [
                    SimpleTweet(
                        tweet.id_str,
                        tweet.user.screen_name,
                        tweet.user.name,
                        tweet.text if self.tweet_mode == "compat" else tweet.full_text,
                        tweet.retweet_count,
                        tweet.favorite_count,
                        tweet.created_at,
                    )
                    for tweet in self.extract_user_top_tweets(author.screen_name, single_author_max_tweets, days_back)
                ],
                authors,
            )
        )

        sorted_top_tweets = heapq.nlargest(tweets_num, tweets, key=lambda tweet: tweet.retweet_count)

        return sorted_top_tweets

    def extract_user_top_tweets(self, username: str, tweets_num: int, days_back: int) -> List[SimpleTweet]:
        self.logger.info(f"Extracting published top tweets for `{username}`...")

        since = datetime.now() - timedelta(days=days_back)
        since = since.strftime("%Y-%m-%d")

        query = f"from:{username} since:{since} -filter:retweets"
        tweets = tweepy.Cursor(self.api.search, q=query, tweet_mode=self.tweet_mode).items()
        top_tweets = heapq.nlargest(tweets_num, tweets, key=lambda tweet: tweet.retweet_count)

        self.logger.info("Tweets extracted")

        return top_tweets
