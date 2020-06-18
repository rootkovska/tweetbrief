import logging
from base64 import b64encode
from typing import List

from yattag import Doc

from exporter.styles import html_style
from qr.qrcoder import QRCoder
from twitterapi.simple_tweet import SimpleTweet
from datetime import date, datetime

class HTMLExporter:
    def __init__(self, url2qrcode: bool = False) -> None:
        self.logger = logging.getLogger(__name__)
        self.doc = Doc()
        self.url2qrcode = url2qrcode

    def as_string(self, tweets: List[SimpleTweet]) -> str:
        self.logger.info("Generating HTML...")

        tag = self.doc.tag
        text = self.doc.text

        with tag("html"):
            with tag("head"):
                self.doc.asis(html_style)
            with tag("h1"):
                text(f"Tweetbrief generated on {datetime.now().strftime('%Y-%m-%d @ %H:%M:%S')}")
            with tag("body"):
                with tag("div", klass="container"):
                    for tweet in tweets:
                        self._tweet2html(tweet)
        html = self.doc.getvalue()

        self.logger.info("HTML generated")
        return html

    def _tweet2html(self, tweet: SimpleTweet) -> None:
        tag = self.doc.tag
        text = self.doc.text

        if self.url2qrcode:
            urls = tweet.extract_urls(remove_http=True)
            tweet.replace_urls("[QR]")

        with tag("div", klass="tweet"):
            with tag("div", klass="tweet-text"):
                with tag("b"):
                    text(f"{tweet.author}: ")
                text(tweet.text)

            if self.url2qrcode:
                qrcoder = QRCoder(box_size=5, border=0)
                for url in urls:
                    with tag("div", klass="tweet-qrcode"):
                        self._inline_svg2data_uri(qrcoder.generate_inline_svg(url))

    def _inline_svg2data_uri(self, inline_svg: str) -> None:
        self.doc.stag("img", src=f"data:image/svg+xml;charset=utf-8;base64,{b64encode(inline_svg).decode()}")
