import logging
import os
from datetime import datetime
from exceptions import TweetBriefError

from exporter.pdf_exporter import PDFExporter
from twitterapi.tweet_extractor import TweetExtractor

log_level = os.getenv("LOG_LEVEL", logging.INFO)
logging.basicConfig(level=log_level)


def main() -> None:
    logger = logging.getLogger(__name__)
    logger.info("Loading parameters...")

    if "TARGET_USERNAME" not in os.environ:
        raise TweetBriefError("TARGET_USERNAME not found!")

    if "CONSUMER_KEY" not in os.environ:
        raise TweetBriefError("CONSUMER_KEY not found!")

    if "CONSUMER_SECRET" not in os.environ:
        raise TweetBriefError("CONSUMER_SECRET not found")

    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    target_username = os.getenv("TARGET_USERNAME")
    single_author_max_tweets = os.getenv("SINGLE_AUTHOR_MAX_TWEETS", 3)
    brief_period = os.getenv("BRIEF_PERIOD", 1)
    brief_max_tweets = os.getenv("BRIEF_MAX_TWEETS", 30)
    brief_dir = os.getenv("BRIEF_DIR", "twitter-briefs")

    try:
        single_author_max_tweets = int(single_author_max_tweets)

        if single_author_max_tweets > 3:
            logger.warning("SINGLE_AUTHOR_MAX_TWEETS is greater than 3! Setting to default...")
            single_author_max_tweets = 3
    except ValueError:
        logger.warning("SINGLE_AUTHOR_MAX_TWEETS must be a number! Setting to default...")
        single_author_max_tweets = 3

    try:
        brief_period = int(brief_period)
    except ValueError:
        logger.warning("BRIEF_PERIOD must be a number! Setting to default...")
        brief_period = 1

    try:
        brief_max_tweets = int(brief_max_tweets)
    except ValueError:
        logger.warning("BRIEF_MAX_TWEETS must be a number! Setting to default...")
        brief_max_tweets = 30

    logger.info("Parameters loaded")
    logger.info("Extracting tweets...")

    extractor = TweetExtractor(consumer_key, consumer_secret, tweet_mode="extended")
    tweets_in_brief = extractor.extract_top_tweets(
        target_username, single_author_max_tweets, brief_max_tweets, brief_period
    )

    logger.info("Exporting brief...")

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{brief_dir}/{target_username}-{today}.pdf"

    exporter = PDFExporter(url2qrcode=True)
    exporter.export(tweets_in_brief, filename)


if __name__ == "__main__":
    main()
