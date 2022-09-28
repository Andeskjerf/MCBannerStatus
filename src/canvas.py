import base64
import io
from PIL import Image, ImageFont

from src.elements.row import RowDirection, RowImage, RowText, TextRow

from .colors import GREEN, RED, WHITE, GREY, BLACK

_DIVIDE_BY_HEIGHT: int = 6


class Canvas:

    image: Image

    field_opacity: float
    field_height: int

    x_offset: float

    text_l: str
    text_r: str

    text_l_col: tuple
    text_r_col: tuple

    font_l: ImageFont
    font_r: ImageFont

    top_left: tuple
    top_right: tuple
    bot_left: tuple
    bot_right: tuple

    bot_left_row: TextRow
    bot_right_row: TextRow

    def __init__(
        self,
        active: bool,
        text_left: str,
        text_right: str,
        name: str,
        favicon: str,
        image_path: str,
        font_regular: str,
        font_italic: str,
        font_size: int,
        x_offset: float,
        opacity: float,
        field_height: int
    ):
        self.bot_left_row = TextRow()
        self.bot_right_row = TextRow(direction=RowDirection.Left)

        self.image = Image.open(image_path).convert("RGB")
        self.text_l = text_left
        self.text_r = text_right

        self.field_height = field_height
        self.field_opacity = opacity

        self.x_offset = x_offset

        self.font_l = ImageFont.truetype(font_regular, font_size)
        self.font_r = self.font_l

        self.text_l_col = GREEN
        self.text_r_col = WHITE

        if not active:
            self.text_l_col = RED
            self.text_r_col = GREY

            if len(font_italic) > 0:
                self.font_r = ImageFont.truetype(font_italic, font_size)

        if not field_height:
            self.field_height = int(self.image.height / _DIVIDE_BY_HEIGHT)

        self.set_positions()

        self.bot_left_row.pos = self.bot_left

        if favicon:
            self.bot_left_row.add(RowImage(
                Image.open(io.BytesIO(base64.b64decode(favicon))),
                font_size + 12
            ))
            self.bot_left_row.add(RowText("", self.font_r, WHITE))

        if name:

            font = font_regular
            if font_italic \
                    and len(font_italic) > 0:
                font = font_italic

            self.bot_left_row.add(
                RowText(
                    name,
                    ImageFont.truetype(font, font_size),
                    WHITE
                )
            )
            self.bot_left_row.add(RowText(" ", self.font_r, WHITE))

        self.bot_left_row.add(RowText(text_left, self.font_l, self.text_l_col))

        self.bot_right_row.pos = self.bot_right
        self.bot_right_row.add(RowText(text_right, self.font_r, self.text_r_col))

        self.draw_image()

    def set_positions(self):
        text_r_w = self.font_r.getbbox(self.text_r)[2]

        y_offset = self.field_height / 2
        right = self.image.width - self.x_offset - text_r_w

        self.top_left = (self.x_offset, y_offset)
        self.top_right = (right, y_offset)

        self.bot_left = (self.x_offset, self.image.height - y_offset)
        self.bot_right = (right, self.image.height - y_offset)

    def draw_overlay(self):
        overlay_opacity = int(255 * self.field_opacity)

        overlay = Image.new(
            "RGBA",
            (self.image.width, self.field_height),
            BLACK+(overlay_opacity,)
        )

        self.image.paste(
            overlay,
            (0, self.image.height - self.field_height),
            overlay
        )

    def draw_image(self):
        self.draw_overlay()
        self.bot_left_row.draw(self.image)
        self.bot_right_row.draw(self.image)

    def save_image(self, target_path: str):
        self.image.convert("RGB").save(target_path)
