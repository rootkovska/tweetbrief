import logging


class PdfExporter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def export(self, tweets):
        self.logger.info("Generating HTML...")

    def _generate_html(self, tweets):
        markup_container = """
            <div class="container">
        """
