import logging
import os
from datetime import datetime
from exceptions import TweetBriefError
from pathlib import Path
from typing import Any

from aws_lambda_context import LambdaContext
from dropbox import Dropbox
from dropbox.exceptions import AuthError, BadInputError

from exporter.pdf_exporter import PDFExporter
from twitterapi.tweet_extractor import TweetExtractor

logger = logging.getLogger()
if logger.hasHandlers():
    logger.setLevel(logging.INFO)
else:
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)


def lambda_handler(event: Any, context: LambdaContext) -> None:
    main()


def main() -> None:
    logger.info("Loading parameters...")

    if "TARGET_USERNAME" not in os.environ:
        raise TweetBriefError("TARGET_USERNAME not found!")

    if "CONSUMER_KEY" not in os.environ:
        raise TweetBriefError("CONSUMER_KEY not found!")

    if "CONSUMER_SECRET" not in os.environ:
        raise TweetBriefError("CONSUMER_SECRET not found!")

    if not any(storage in os.environ for storage in ["BRIEF_OUTPUT", "DROPBOX_ACCESS_TOKEN"]):
        raise TweetBriefError("No storage provided!")

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
    brief_output = os.getenv("BRIEF_OUTPUT", None)
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

    if brief_output is not None:
        try:
            brief_output = Path(brief_output)
            if not brief_output.is_dir():
                brief_output.mkdir(parents=True)
            if not os.access(brief_output, os.W_OK):
                raise PermissionError(f"No write permissions on `{brief_output}`!")
        except (FileExistsError, PermissionError):
            logger.error(f"The path `{brief_output}` is broken!")
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
    date_str = datetime.now().strftime('%Y-%m-%d')
    period_desc = "Daily" if brief_period == 1 else \
                  "Weekly" if brief_period == 7 else \
                  "Monthly" if 30 <= brief_period <= 31 else \
                  f"Last {brief_period} days"

    title = f"{period_desc} Twitter Brief for @{target_username} ({date_str})"
    subtitle = f"Excluding RTs, top {single_author_max_tweets} tweets/author, {datetime.now().strftime('%H:%M:%S UTC')}"
    pdf = exporter.export(tweets_in_brief, title=title, subtitle=subtitle)

    filename = f"tweetbrief-{target_username}-{period_desc.lower()}-{date_str}.pdf"
    if brief_output is not None:
        logger.info("Saving locally...")

        brief_path = brief_output / filename
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
