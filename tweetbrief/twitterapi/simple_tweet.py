import html
from typing import List

from utils.regex_patterns import http_pattern, url_pattern


class SimpleTweet:
    def __init__(self, author: str, text: str, retweet_count: int) -> None:
        self.author = author
        self.text = self._cleanse(text)
        self.retweet_count = retweet_count

    def extract_urls(self, remove_http: bool = False) -> List[str]:
        urls = url_pattern.findall(self.text)
        if remove_http:
            urls = list(map(lambda url: http_pattern.sub("", url), urls))

        return urls

    def replace_urls(self, value) -> None:
        self.text = url_pattern.sub(value, self.text)

    def _cleanse(self, text: str) -> str:
        return " ".join(html.unescape(text).split())
