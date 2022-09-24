from enum import Enum
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from src.colors import BLACK


_BLUR_RADIUS: int = 8
_BLUR_COLOR = BLACK
_BLUR_PASSES = 2


class RowDirection(Enum):
    Left = 0
    Right = 1


class RowText:

    text: str
    font: ImageFont
    color: tuple
    width: int
    height: int
    x: int
    y: int
    bbox: tuple

    def __init__(
        self,
        text,
        font,
        color
    ) -> None:
        self.text = text
        self.font = font
        self.color = color

        self.bbox = self.font.getbbox(self.text)
        self.x = self.bbox[0]
        self.y = self.bbox[1]
        self.width = self.bbox[2]
        self.height = self.bbox[3]

    def draw(self, position, image):
        blurred = Image.new("RGBA", image.size)

        # Draw blurred text until _BLUR_PASSES, then draw normal text
        i = 0
        while i <= _BLUR_PASSES:
            blur = i < _BLUR_PASSES
            draw = ImageDraw.Draw(blurred if blur else image)

            draw.text(
                position,
                self.text,
                _BLUR_COLOR if blur else self.color,
                anchor="lm",
                font=self.font
            )

            if blur:
                blurred = blurred.filter(ImageFilter.BoxBlur(_BLUR_RADIUS))
                image.paste(blurred, blurred)

            i += 1


class RowImage:

    image: Image
    width: int

    def __init__(self, img: Image, size) -> None:
        img = img.resize((size, size))

        self.image = img
        self.width = img.width
        self.height = img.height

        bigsize = (img.size[0] * 3, img.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(img.size, Image.ANTIALIAS)
        self.image.putalpha(mask)

    def draw(self, position, image):
        image.paste(self.image, (position[0], position[1] - int(self.height / 2)), self.image)


class TextRow:

    children: list
    pos: tuple
    direction: RowDirection

    def __init__(
        self,
        pos=(0, 0),
        direction=RowDirection.Right
    ) -> None:
        self.children = []
        self.pos = pos
        self.direction = direction

    def add(self, child):
        self.children.append(child)

    def draw(self, image: Image):

        x_offset = int(self.pos[0])
        y_offset = int(self.pos[1])

        for child in self.children:
            child.draw((x_offset, y_offset), image)

            if self.direction == RowDirection.Left:
                x_offset -= child.width - 16
            else:
                x_offset += child.width + 16
