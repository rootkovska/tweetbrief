import logging
import xml.etree.ElementTree as ET

from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from qrcode.image.svg import SvgFragmentImage


class QRCoder:
    def __init__(self, box_size: int = 10, border: int = 4) -> None:
        self.logger = logging.getLogger(__name__)
        self.qr = QRCode(
            error_correction=ERROR_CORRECT_L, box_size=box_size, border=border, image_factory=SvgFragmentImage,
        )

    def generate_inline_svg(self, text: str) -> str:
        self.qr.add_data(text)

        qrcode = self.qr.make_image().get_image()
        inline_svg = ET.tostring(qrcode)

        self.qr.clear()

        return inline_svg
