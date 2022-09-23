import os
import re


def sanitize_float(string: str):
    return re.sub(r"[,]\b", ".", string)


def is_float(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_image(path: str):
    if not path:
        raise Exception("Image path not specified")
    res = re.findall(r"\.(png|jpg|jpeg|bmp)$", path.lower())
    return len(res) > 0


def is_font(path: str):
    if not path:
        raise Exception("Font path not specified")
    res = re.findall(r"\.(ttf|otf)$", path.lower())
    return len(res) > 0


def file_exists(path: str) -> None:
    if not os.path.exists(path):
        raise Exception("File does not exist: " + path)
