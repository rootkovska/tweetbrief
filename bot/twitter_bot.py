import logging
import os

from brief_generator import BriefGenerator
from exception import TwitterBotError
from twitter_extractor import TwitterExtractor

log_level = os.getenv("LOG_LEVEL", logging.INFO)
logging.basicConfig(level=log_level)


def main():
    logger = logging.getLogger(__name__)
    logger.info("Loading bot parameters...")

    if "TARGET_USERNAME" not in os.environ:
        logger.error("Username is misssing!")
        raise TwitterBotError("TARGET_USERNAME not found")

    if "CONSUMER_KEY" not in os.environ or "CONSUMER_SECRET" not in os.environ:
        logger.error("API keys are missing!")
        raise KeyError("CONSUMER_KEY or/and CONSUMER_SECRET not found")

    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    target_username = os.getenv("TARGET_USERNAME")
    single_author_max_tweets = os.getenv("SINGLE_AUTHOR_MAX_TWEETS", 3)
    brief_period = os.getenv("BRIEF_PERIOD", 1)

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

    logger.info("Parameters loaded")

    logger.info("Extracting tweets...")
    extractor = TwitterExtractor(consumer_key, consumer_secret)
    tweets_in_brief = extractor.extract_tweets(target_username, single_author_max_tweets, brief_period)

    logger.info("Generating brief...")
    generator = BriefGenerator()
    generator.generate_pdf(tweets_in_brief)


if __name__ == "__main__":
    main()
