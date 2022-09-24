from PIL import Image, ImageDraw, ImageFont, ImageFilter

from .colors import GREEN, RED, WHITE, GREY, BLACK

_DIVIDE_BY_HEIGHT: int = 6

_BLUR_RADIUS: int = 8
_BLUR_COLOR = BLACK
_BLUR_PASSES = 2


class Canvas:

    favicon: Image
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

    def __init__(
        self,
        active: bool,
        text_left: str,
        text_right: str,
        description: str,
        favicon: str,
        image_path: str,
        font_regular: str,
        font_italic: str,
        font_size: int,
        x_offset: float,
        opacity: float,
        field_height: int
    ):
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
        self.draw_image()

    def set_positions(self):
        width = self.image.width
        height = self.image.height

        text_r_w = self.font_r.getbbox(self.text_r)[2]

        y_offset = self.field_height / 2
        right = width - self.x_offset - text_r_w

        self.top_left = (self.x_offset, y_offset)
        self.top_right = (right, y_offset)

        self.bot_left = (self.x_offset, height - y_offset)
        self.bot_right = (right, height - y_offset)

    def draw_overlay(self):
        width = self.image.width
        height = self.image.height
        overlay_opacity = int(255 * self.field_opacity)

        overlay = Image.new(
            "RGBA",
            (width, self.field_height),
            BLACK+(overlay_opacity,)
        )

        self.image.paste(
            overlay,
            (0, height - self.field_height),
            overlay
        )

    def draw_text(self, left_pos, right_pos):
        blurred = Image.new("RGBA", self.image.size)

        # Draw blurred text until _BLUR_PASSES, then draw normal text
        i = 0
        while i <= _BLUR_PASSES:
            blur = i < _BLUR_PASSES
            draw = ImageDraw.Draw(blurred if blur else self.image)

            draw.text(
                left_pos,
                self.text_l,
                _BLUR_COLOR if blur else self.text_l_col,
                anchor="lm",
                font=self.font_l
            )
            draw.text(
                right_pos,
                self.text_r,
                _BLUR_COLOR if blur else self.text_r_col,
                anchor="lm",
                font=self.font_r
            )

            if blur:
                blurred = blurred.filter(ImageFilter.BoxBlur(_BLUR_RADIUS))
                self.image.paste(blurred, blurred)

            i += 1

    def draw_image(self):
        self.draw_overlay()
        self.draw_text(self.bot_left, self.bot_right)

    def save_image(self, target_path: str):
        self.image.convert("RGB").save(target_path)
