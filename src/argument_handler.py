import re
import sys

from src import utils

from src.conf import (
    FIELD_HEIGHT,
    FIELD_OPACITY,
    FONT_SIZE,
    IMAGE_PATH,
    ITALIC_FONT_PATH,
    OFFLINE_TEXT,
    ONLINE_TEXT,
    PLAYER_COUNT_OFFLINE_TEXT,
    REGULAR_FONT_PATH,
    SERVER_HOST,
    SERVER_PORT,
    X_OFFSET,
    TARGET_PATH,
    IMAGE_ROTATION,
    IMAGE_ROTATION_INTERVAL
)


class ArgumentHandler:

    name: str
    args: list

    host: str = SERVER_HOST
    port: int = SERVER_PORT

    x_offset: float = X_OFFSET or 64
    height: int = int(FIELD_HEIGHT) if FIELD_HEIGHT is not None else None
    opacity: float = FIELD_OPACITY if FIELD_OPACITY is not None else 0.5

    image_path: str = IMAGE_PATH
    image_rotation: bool = IMAGE_ROTATION or False
    image_rotation_interval: int = IMAGE_ROTATION_INTERVAL or 900
    target: str = TARGET_PATH or ""

    font_size: int = FONT_SIZE or 64
    font_regular_path: str = REGULAR_FONT_PATH
    font_italic_path: str = ITALIC_FONT_PATH or ""

    online_text: str = ONLINE_TEXT or "NOT SET"
    offline_text: str = OFFLINE_TEXT or "NOT SET"
    player_offline_text: str = PLAYER_COUNT_OFFLINE_TEXT or "NOT SET"

    force_update: bool = False

    def __init__(self) -> None:
        self.name = re.findall(r"[^\/]+\b$", sys.argv[0])[0]
        self.args = sys.argv[1:]

        self.print_help()
        self.parse_arguments()

        try:
            self.check_values()
        except Exception as e:
            print(e)
            print("Use --help for more information")
            exit()

    def print_help(self) -> None:
        if "--help" in self.args:

            print(f"Usage: {self.name} [options]\n"
                  "    Paths:\n"
                  "        --images\t\t\tEnable image rotation using images folder\n"
                  "        --interval <sec>\t\tHow often should the image be rotated out, in seconds\n"
                  "        -b --image <path>\t\tPath to base image\n"
                  "        -r --font-regular <path>\tPath to regular font\n"
                  "        -i --font-italic <path>\t\tPath to italic font\n"
                  "        -t --target <path>\t\tPath to save the image to\n"
                  "\n"
                  "    Text:\n"
                  "        -e --offline-text <text>\tText to display if server is unreachable\n"
                  "        -a --online-text <text>\t\tText to display if connection succeeds\n"
                  "        -p --player-text <text>\t\tText to display for player count if connection fails\n"
                  "        -s --font-size <size>\t\tFont size for the text\n"
                  "        -x --x-offset <offset>\t\tText offset from the edges of the image\n"
                  "        -h --height <height>\t\tHeight of the text field\n"
                  "        -o --opacity <opacity>\t\tOpacity of the text field\n"
                  "\n"
                  "    Host:\n"
                  "        --host <host>\t\t\tHost to connect to\n"
                  "        --port <port>\t\t\tPort to connect to\n"
                  "\n"
                  "    --force\t\t\t\tForce image to update\n"
                  "    --help\t\t\t\tShow this help message\n"
                  "\n"
                  "    Permanent options can be set in conf.py\n"
                  )
            exit()

    def parse_arguments(self):

        i = 0

        while i < len(self.args):

            arg = self.args[i]
            matched = True

            match arg:
                case "-s" | "--font-size":
                    self.font_size = self.parse_int(self.next_arg(i), arg)
                case "-t" | "--target":
                    self.target = self.next_arg(i)
                case "-x" | "--x-offset":
                    self.x_offset = self.parse_float(self.next_arg(i), arg)
                case "-h" | "--height":
                    self.height = self.parse_int(self.next_arg(i), arg)
                case "-o" | "--opacity":
                    self.opacity = self.parse_float(self.next_arg(i), arg)
                case "-a" | "--online-text":
                    self.online_text = self.next_arg(i)
                case "-e" | "--offline-text":
                    self.offline_text = self.next_arg(i)
                case "-b" | "--image":
                    self.image_path = self.next_arg(i)
                case "-r" | "--font-regular":
                    self.font_regular_path = self.next_arg(i)
                case "-i" | "--font-italic":
                    self.font_italic_path = self.next_arg(i)
                case "-p" | "--player-text":
                    self.player_offline_text = self.next_arg(i)
                case "--host":
                    self.host = self.next_arg(i)
                case "--port":
                    self.port = self.parse_int(self.next_arg(i), arg)
                case "--interval":
                    self.image_rotation_interval = self.parse_int(self.next_arg(i), arg)
                case "--images":
                    self.image_rotation = True
                    matched = False
                case "--force":
                    self.force_update = True
                    matched = False
                case _:
                    matched = False

            if matched:
                i += 2
            else:
                i += 1

    def check_values(self):
        if not self.target \
                or len(self.target) == 0:
            raise Exception("Target path not specified\n"
                            "Set it with -t, --target or modify conf.py")

        # Make sure the paths given are valid
        if not self.image_rotation \
                and not utils.is_image(self.image_path):
            raise Exception("Invalid image path: " + self.image_path)

        if not utils.is_font(self.font_regular_path):
            raise Exception("Invalid font path: " + self.font_regular_path)

        if len(self.font_italic_path) > 0 \
                and not utils.is_font(self.font_italic_path):
            raise Exception("Invalid font path: " + self.font_italic_path)

        if not utils.has_valid_extension(self.target):
            raise Exception(f"Invalid image extension: {self.target}\n"
                            "Valid extensions: " + ", ".join(utils.VALID_EXTENSIONS))

    def next_arg(self, i: int) -> str:
        if len(self.args) > i + 1:
            arg = self.args[i + 1]
            if arg.startswith("-"):
                raise Exception(f"Missing argument for {self.args[i]}")
            return arg
        raise Exception(f"Missing argument for {self.args[i]}")

    def parse_int(self, input, arg: str = "") -> int:
        if type(input) is int:
            return input

        if not input.isdigit():
            raise Exception(f"Expected number for {arg}: {input}")
        return int(input)

    def parse_float(self, input, arg: str = "") -> float:
        if type(input) is int \
                or type(input) is float:
            return input

        input = utils.sanitize_float(input)
        if not utils.is_float(input):
            raise Exception(f"Expected number/float for {arg}: {input}")
        return float(input)
