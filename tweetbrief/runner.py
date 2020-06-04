import logging
import os
from datetime import datetime
from exceptions import TweetBriefError
from pathlib import Path

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
        raise TweetBriefError("CONSUMER_SECRET not found!")

    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    target_username = os.getenv("TARGET_USERNAME")
    single_author_max_tweets = os.getenv("SINGLE_AUTHOR_MAX_TWEETS", 3)
    brief_period = os.getenv("BRIEF_PERIOD", 1)
    brief_max_tweets = os.getenv("BRIEF_MAX_TWEETS", 30)
    brief_path = os.getenv("BRIEF_PATH", os.getcwd())
    url2qrcode = os.getenv("URL2QR", True)

    try:
        single_author_max_tweets = int(single_author_max_tweets)

        if single_author_max_tweets > 3:
            logger.warning("SINGLE_AUTHOR_MAX_TWEETS is greater than 3! Setting to default (3)...")
            single_author_max_tweets = 3
    except ValueError:
        logger.warning("SINGLE_AUTHOR_MAX_TWEETS must be an integer! Setting to default (3)...")
        single_author_max_tweets = 3

    try:
        brief_period = int(brief_period)
    except ValueError:
        logger.warning("BRIEF_PERIOD must be an integer! Setting to default (1)...")
        brief_period = 1

    try:
        brief_max_tweets = int(brief_max_tweets)
    except ValueError:
        logger.warning("BRIEF_MAX_TWEETS must be an integer! Setting to default (30)...")
        brief_max_tweets = 30

    try:
        if not os.path.isdir(brief_path):
            Path(brief_path).mkdir(parents=True)
        if not os.access(brief_path, os.W_OK):
            raise PermissionError(f"No write permissions on `{brief_path}`!")
    except (FileExistsError, PermissionError):
        logger.exception(f"Wrong path `{brief_path}`!")

    if not isinstance(url2qrcode, bool):
        logger.warning("URL2QR must be a boolean!Setting to default (True)...")
        url2qrcode = True

    logger.info("Parameters loaded")
    logger.info("Extracting tweets...")

    extractor = TweetExtractor(consumer_key, consumer_secret, tweet_mode="extended")
    tweets_in_brief = extractor.extract_top_tweets(
        target_username, single_author_max_tweets, brief_max_tweets, brief_period
    )

    logger.info("Exporting brief...")

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{brief_path}/{target_username}-{today}.pdf"

    exporter = PDFExporter(url2qrcode)
    exporter.export(tweets_in_brief, filename)


if __name__ == "__main__":
    main()
