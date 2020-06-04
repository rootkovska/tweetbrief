import logging
import os
from datetime import datetime
from exceptions import TweetBriefError
from pathlib import Path

from dropbox import Dropbox
from dropbox.exceptions import AuthError, BadInputError

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

    if not any(storage in os.environ for storage in ["LOCAL_PATH", "DROPBOX_ACCESS_TOKEN"]):
        raise TweetBriefError("No storage found!")

    # Twitter API parameters
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")

    # bot parameters
    target_username = os.getenv("TARGET_USERNAME")
    single_author_max_tweets = os.getenv("SINGLE_AUTHOR_MAX_TWEETS", 3)
    brief_period = os.getenv("BRIEF_PERIOD", 1)
    brief_max_tweets = os.getenv("BRIEF_MAX_TWEETS", 30)
    url2qrcode = os.getenv("URL2QR", True)

    # storage parameters
    local_path = os.getenv("LOCAL_PATH", None)
    dropbox_access_token = os.getenv("DROPBOX_ACCESS_TOKEN", None)

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

    if not isinstance(url2qrcode, bool):
        logger.warning("URL2QR must be a boolean!Setting to default (True)...")
        url2qrcode = True

    if local_path is not None:
        try:
            local_path = Path(local_path)
            if not local_path.is_dir():
                local_path.mkdir(parents=True)
            if not os.access(local_path, os.W_OK):
                raise PermissionError(f"No write permissions on `{local_path}`!")
        except (FileExistsError, PermissionError):
            logger.error(f"The path `{local_path}` is broken!")
            raise

    if dropbox_access_token is not None:
        try:
            dbx = Dropbox(dropbox_access_token)
            dbx.users_get_current_account()
        except (AuthError, BadInputError):
            logger.error("`DROPBOX_ACCESS_TOKEN` is invalid!")
            raise

    logger.info("Parameters loaded")
    logger.info("Extracting tweets...")

    extractor = TweetExtractor(consumer_key, consumer_secret, tweet_mode="extended")
    tweets_in_brief = extractor.extract_top_tweets(
        target_username, single_author_max_tweets, brief_max_tweets, brief_period
    )

    logger.info("Exporting brief...")

    exporter = PDFExporter(url2qrcode)
    pdf = exporter.export(tweets_in_brief)

    filename = f"{target_username}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    if local_path is not None:
        logger.info("Saving locally...")

        brief_path = local_path / filename
        with open(brief_path, "wb") as f:
            f.write(pdf.getbuffer())

        logger.info("Brief saved")
    if dropbox_access_token is not None:
        logger.info("Uploading to Dropbox...")

        brief_path = Path("/") / filename
        dbx.files_upload(pdf.getvalue(), brief_path.as_posix())

        logger.info("Brief uploaded")


if __name__ == "__main__":
    main()
