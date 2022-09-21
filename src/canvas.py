from PIL import Image, ImageDraw, ImageFont
from .colors import GREEN, RED, WHITE, GREY, BLACK


class Canvas:

    DIVIDE_BY_HEIGHT = 6

    image: Image
    field_transparency: float = 0.5
    field_height: float
    font_regular: ImageFont
    font_italic: ImageFont

    def __init__(self, image_path: str, font_regular: str, font_italic: str, font_size: int):
        self.image = Image.open(image_path).convert("RGBA")
        self.field_height = self.image.height / self.DIVIDE_BY_HEIGHT
        self.font_regular = ImageFont.truetype(font_regular, font_size)
        if len(font_italic) == 0:
            self.font_italic = self.font_regular
        else:
            self.font_italic = ImageFont.truetype(font_italic, font_size)


    def draw_overlay(self):
        overlay_opacity = int(255 * self.field_transparency)

        overlay = Image.new("RGBA", self.image.size, BLACK+(0,))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle(
            ((0, self.image.height), (self.image.width, self.image.height - self.field_height)),
            fill=BLACK+(overlay_opacity, )
        )

        return Image.alpha_composite(self.image, overlay)


    def draw_text(self, status):
        draw = ImageDraw.Draw(self.image)

        text_right = status.get_player_count()

        text_right_w = self.font_regular.getbbox(text_right)[2]
        text_right_h = self.font_regular.getbbox(text_right)[3]

        y_offset = self.image.height - (self.field_height / 2) - (text_right_h / 2)
        x_offset = 64
        bottom_right = (self.image.width - x_offset - text_right_w, y_offset)
        bottom_left = (x_offset, y_offset)


        draw.text(
            bottom_left,
            status.get_status(),
            GREEN if status.active else RED,
            font=self.font_regular
        )

        draw.text(
            bottom_right,
            text_right,
            WHITE if status.active else GREY,
            font=self.font_regular if status.active else self.font_italic
        )


    def get_image(self, status):
        self.image = self.draw_overlay()
        self.draw_text(status)
        return self.image
