from enum import Enum
import os
import re
import sys

from src import Canvas, Status
from src.conf import IMAGE_PATH, ITALIC_FONT_PATH, REGULAR_FONT_PATH


class ArgType(Enum):
    FONT_SIZE = 0
    TARGET_PATH = 1


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
        ArgType.TARGET_PATH: None
        }

    name = re.findall(r"[^\/]+\b$", sys.argv[0])[0]
    args = sys.argv[1:]

    if len(args) < 2:
        print(f"Usage: {name} [options]\n"
              "    -s --font-size <size>\tFont size for the text\n"
              "    -t --target <path>\t\tPath to save the image to")
        exit()

    font_size_found = False
    target_path_found = False

    for arg in args:

        if arg == "-s" or arg == "--font-size":
            font_size_found = True
            continue

        elif font_size_found:
            try:
                result[ArgType.FONT_SIZE] = int(arg)
                font_size_found = False
            except:
                raise Exception("Invalid font size, expected number: " + arg)
            continue

        elif arg == "-t" or arg == "--target":
            target_path_found = True
            continue

        elif target_path_found:
            result[ArgType.TARGET_PATH] = arg
            target_path_found = True
            continue

    if result[ArgType.TARGET_PATH] is None:
        raise Exception("Target path not specified")

    return result


def main():

    status = Status()

    try:

        arguments = handle_arguments()
        font_size = arguments[ArgType.FONT_SIZE]
        target = arguments[ArgType.TARGET_PATH]

        if not is_image(IMAGE_PATH):
            raise Exception("Invalid image path: " + IMAGE_PATH)
        if not is_font(REGULAR_FONT_PATH):
            raise Exception("Invalid font path: " + REGULAR_FONT_PATH)
        if len(ITALIC_FONT_PATH) > 0 and not is_font(ITALIC_FONT_PATH):
            raise Exception("Invalid font path: " + ITALIC_FONT_PATH)

        canvas = Canvas(IMAGE_PATH, REGULAR_FONT_PATH, ITALIC_FONT_PATH, font_size)
        img = canvas.get_image(status)
        img.convert("RGB").save(target)

    except Exception as e:

        print("Exception raised:\n"
              f"    {e}"
        )


if __name__ == "__main__":
    main()
