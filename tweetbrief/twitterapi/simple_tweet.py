import html
from typing import List

import emoji

from utils.regex_patterns import http_pattern, url_pattern


class SimpleTweet:
    def __init__(
        self, id: str, uid: str, author: str, text: str, retweet_count: int, favorite_count: int, created_at: str
    ) -> None:
        self.id = id
        self.uid = uid
        self.author = author
        self.text = self._cleanse(text)
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.created_at = created_at

    def extract_urls(self, remove_http: bool = False) -> List[str]:
        urls = url_pattern.findall(self.text)
        if remove_http:
            urls = list(map(lambda url: http_pattern.sub("", url), urls))

        return urls

    def replace_urls(self, value) -> None:
        self.text = url_pattern.sub(value, self.text)

    def _cleanse(self, text: str) -> str:
        cleansed_text = " ".join(html.unescape(text).split())
        cleansed_text = emoji.demojize(cleansed_text)
        return cleansed_text
