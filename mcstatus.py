from enum import Enum
import re
import sys

from src import Canvas, Status, utils
from src.conf import (
    FIELD_HEIGHT,
    FIELD_OPACITY,
    FONT_SIZE,
    IMAGE_PATH,
    ITALIC_FONT_PATH,
    REGULAR_FONT_PATH,
    X_OFFSET
)


VALID_EXTENSIONS = [
    "png",
    "jpg",
    "jpeg",
    "bmp"
]


def has_valid_extension(path: str) -> bool:
    return path.lower().endswith(tuple(VALID_EXTENSIONS))


class ArgType(Enum):
    FONT_SIZE = 0
    TARGET_PATH = 1
    X_OFFSET = 2
    FIELD_HEIGHT = 3
    FIELD_OPACITY = 4


def handle_arguments() -> dict:
    result = {
        ArgType.FONT_SIZE: FONT_SIZE,
        ArgType.TARGET_PATH: None,
        ArgType.X_OFFSET: X_OFFSET,
        ArgType.FIELD_HEIGHT: FIELD_HEIGHT,
        ArgType.FIELD_OPACITY: FIELD_OPACITY,
    }

    name = re.findall(r"[^\/]+\b$", sys.argv[0])[0]
    args = sys.argv[1:]

    if len(args) < 2 or \
        "--help" in args or \
            "-t" not in args:

        if "-t" not in args:
            print("Missing target path argument")

        print(f"Usage: {name} [options] -t path\n"
              "    -s --font-size <size>\tFont size for the text\n"
              "    -t --target <path>\t\tPath to save the image to\n"
              "    -x --x-offset <offset>\tText offset from the edges of the image\n"
              "    -h --height <height>\tHeight of the text field\n"
              "    -o --opacity <opacity>\tOpacity of the text field\n"
              "\n    --help\t\t\tShow this help message\n"
              )
        exit()

    looking_for = None

    for arg in args:

        text: str = ""

        match arg:
            case "-s" | "--font-size":
                looking_for = ArgType.FONT_SIZE
                text = "font size"
                continue
            case "-t" | "--target":
                looking_for = ArgType.TARGET_PATH
                continue
            case "-x" | "--x-offset":
                looking_for = ArgType.X_OFFSET
                text = "X offset"
                continue
            case "-h" | "--height":
                looking_for = ArgType.FIELD_HEIGHT
                text = "height"
                continue
            case "-o" | "--opacity":
                looking_for = ArgType.FIELD_OPACITY
                text = "opacity"
                continue

        match looking_for:
            case ArgType.FONT_SIZE:
                if not arg.isdigit():
                    raise Exception(f"Expected number for {text}: {arg}")
                result[looking_for] = int(arg)

            case ArgType.FIELD_OPACITY \
                | ArgType.FIELD_HEIGHT \
                    | ArgType.X_OFFSET:
                arg = utils.sanitize_float(arg)
                if not utils.is_float(arg):
                    raise Exception(f"Expected number/float for {text}: {arg}")
                result[looking_for] = float(arg)

            case ArgType.TARGET_PATH:
                result[looking_for] = arg

        looking_for = None

    if result[ArgType.TARGET_PATH] is None:
        raise Exception("Target path not specified")

    return result


def main():

    # Make sure the paths given are valid
    if not utils.is_image(IMAGE_PATH):
        raise Exception("Invalid image path: " + IMAGE_PATH)
    if not utils.is_font(REGULAR_FONT_PATH):
        raise Exception("Invalid font path: " + REGULAR_FONT_PATH)
    if len(ITALIC_FONT_PATH) > 0 and not utils.is_font(ITALIC_FONT_PATH):
        raise Exception("Invalid font path: " + ITALIC_FONT_PATH)

    status = Status()

    # Only update the image if there's any new data
    if not status.updated:
        print("No new data, skipping")
        exit()

    try:

        arguments = handle_arguments()
        font_size = arguments[ArgType.FONT_SIZE]
        target = arguments[ArgType.TARGET_PATH]
        x_offset = arguments[ArgType.X_OFFSET]
        height = arguments[ArgType.FIELD_HEIGHT]
        opacity = arguments[ArgType.FIELD_OPACITY]

        if not has_valid_extension(target):
            raise Exception(f"Invalid image extension: {target}\n"
                            "Valid extensions: " + ", ".join(VALID_EXTENSIONS))

        Canvas(
            status,
            IMAGE_PATH,
            REGULAR_FONT_PATH,
            ITALIC_FONT_PATH,
            font_size,
            x_offset,
            opacity,
            height
        ).save_image(target)

    except Exception as e:

        print("Exception raised:\n"
              f"{e}")


if __name__ == "__main__":
    main()
