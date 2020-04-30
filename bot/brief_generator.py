import datetime
import logging
import re

from bleach import linkify
from weasyprint import CSS, HTML
from weasyprint.fonts import FontConfiguration
from weasyprint.formatting_structure.boxes import BlockBox

html_style = """
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Noto+Sans:ExtraCondensed+ExtraLight" />
<style>
    .container {
        columns: 2;
        column-gap: 5px;
        column-fill: balance;
    }
    .tweet {
        margin: 5px 0;
        padding: 2.5px;
        border-radius: 2.5px;
        background-color: lightskyblue;
        font-family: "Noto Sans", sans-serif;
        font-size: 5px;
        line-height: 1.15;
    }

    .container .tweet:nth-child(odd) {
        background-color: whitesmoke;
    }
</style>
"""

pdf_style = """
    @page {
        size: A4;
        margin: 5mm;
    }
"""


class BriefGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_pdf(self, tweets):
        self.logger.info("Generating HTML...")
        html = self.__generate_html(tweets)

        self.logger.info("Configuring PDF settings...")
        css = CSS(string=pdf_style)

        self.logger.info("Creating PDF...")
        pdf = HTML(string=html).render(stylesheets=[css])

        self.logger.info("Updating height to fit on one page")
        needed_height = len(pdf.pages) * 297
        new_pdf_style = pdf_style.replace("A4", f"210mm {needed_height}mm")
        new_css = CSS(string=new_pdf_style)

        self.logger.info("Saving to PDF...")
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        filename = f"/output/tweets-{today}.pdf"
        HTML(string=html).write_pdf(target=filename, stylesheets=[new_css])

    def __generate_html(self, tweets):
        container = """<div class="container">"""
        for tweet in tweets:
            author = self.__cleanse(tweet.author)
            text = self.__cleanse(tweet.text)
            text = linkify(text)

            container = (
                container
                + f"""
                    <div class="tweet">
                        <b>{author}:</b> {text}
                    </div>
                """
            )
        container = container + "</div>"

        html = f"""
            <html>
            <head>
                <meta charset="UTF-8" />
                {html_style}
            </head>
            <body>
                {container}
            </body>
            </html>
        """

        return html

    def __cleanse(self, text):
        return " ".join(text.split())
