import logging
import re
from io import BytesIO
from typing import List

from weasyprint import CSS, HTML

from exporter.html_exporter import HTMLExporter
from exporter.styles import pdf_style
from twitterapi.simple_tweet import SimpleTweet


class PDFExporter:
    def __init__(self, url2qrcode: bool = False) -> None:
        self.logger = logging.getLogger(__name__)
        self.html_exporter = HTMLExporter(url2qrcode)

    def export(self, tweets: List[SimpleTweet]) -> BytesIO:
        self.logger.info("Generating PDF...")

        pdf = BytesIO()
        html = self.html_exporter.as_string(tweets)
        style = CSS(string=pdf_style)
        HTML(string=html).write_pdf(pdf, stylesheets=[style])

        self.logger.info("PDF generated")

        return pdf
