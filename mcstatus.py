from enum import Enum
import os
import re
import sys

from src import Canvas, Status
from src.conf import IMAGE_PATH, ITALIC_FONT_PATH, REGULAR_FONT_PATH


class ArgType(Enum):
    FONT_SIZE = 0
    TARGET_PATH = 1
    X_OFFSET = 2


def is_image(path: str):
    res = re.findall(r"\.(png|jpg|jpeg|bmp)$", path.lower())
    return len(res) > 0


def is_font(path: str):
    res = re.findall(r"\.(ttf|otf)$", path.lower())
    return len(res) > 0


def file_exists(path: str):
    if not os.path.exists(path):
        raise Exception("File does not exist: " + path)


def handle_arguments():
    result = {
        ArgType.FONT_SIZE: 64,
        ArgType.TARGET_PATH: None,
        ArgType.X_OFFSET: 64
        }

    name = re.findall(r"[^\/]+\b$", sys.argv[0])[0]
    args = sys.argv[1:]

    if len(args) < 2:
        print(f"Usage: {name} [options] -t path\n"
              "    -s --font-size <size>\tFont size for the text\n"
              "    -t --target <path>\t\tPath to save the image to\n"
              "    -x --x-offset <offset>\tOffset from the edges of the image\n")
        exit()

    looking_for = None

    for arg in args:

        if arg == "-s" or arg == "--font-size":
            looking_for = ArgType.FONT_SIZE
            continue

        elif arg == "-t" or arg == "--target":
            looking_for = ArgType.TARGET_PATH
            continue

        elif arg == "-o" or arg == "--offset":
            looking_for = ArgType.X_OFFSET
            continue

        match looking_for:
            case ArgType.FONT_SIZE:
                result[looking_for] = int(arg)

            case ArgType.TARGET_PATH:
                result[looking_for] = arg

            case ArgType.X_OFFSET:
                result[looking_for] = int(arg)

        looking_for = None

    if result[ArgType.TARGET_PATH] is None:
        raise Exception("Target path not specified")

    return result


def main():

    # Make sure the paths given are valid
    if not is_image(IMAGE_PATH):
        raise Exception("Invalid image path: " + IMAGE_PATH)
    if not is_font(REGULAR_FONT_PATH):
        raise Exception("Invalid font path: " + REGULAR_FONT_PATH)
    if len(ITALIC_FONT_PATH) > 0 and not is_font(ITALIC_FONT_PATH):
        raise Exception("Invalid font path: " + ITALIC_FONT_PATH)

    status = Status()

    try:

        arguments = handle_arguments()
        font_size = arguments[ArgType.FONT_SIZE]
        target = arguments[ArgType.TARGET_PATH]
        x_offset = arguments[ArgType.X_OFFSET]

        Canvas(
            status,
            IMAGE_PATH,
            REGULAR_FONT_PATH,
            ITALIC_FONT_PATH,
            font_size,
            x_offset
        ).save_image(target)

    except Exception as e:

        print("Exception raised:\n"
              f"    {e}"
        )


if __name__ == "__main__":
    main()
