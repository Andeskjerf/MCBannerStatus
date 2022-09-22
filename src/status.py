import re
import json
from mcrcon import MCRcon
from .conf import MCRCON_HOST, MCRCON_PASSWORD, MCRCON_PORT


class Data:

    max_players: int = 0
    online_players: int = 0
    active: bool = False

    def __init__(self, max_players, online_players, active):
        self.max_players = max_players
        self.online_players = online_players
        self.active = active

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Status:

    data: Data = Data(0, 0, False)
    cache: str = None
    updated = False

    def __init__(self):
        self.read_cache()

        try:
            with MCRcon(MCRCON_HOST, MCRCON_PASSWORD, port=MCRCON_PORT) as mcr:
                res = mcr.command("list").splitlines(keepends=False)
                nums = re.findall(r"[0-9]+", res[0])

                if len(nums) >= 2:
                    self.data.online_players = int(nums[0])
                    self.data.max_players = int(nums[1])
                    self.data.active = True
                else:
                    raise Exception("Could not parse player count")
        except:
            self.data.online_players = 0
            self.data.max_players = 0
            self.data.active = False

        self.updated = self.has_changed()
        if self.updated:
            self.write_cache()

    def get_player_count(self):
        if not self.data.active:
            return "Unable to establish connection"
        return f"{self.data.online_players} / {self.data.max_players}"

    def get_status(self):
        if not self.data.active:
            return "Offline"
        return "Online"

    def has_changed(self):
        return self.data.to_json() != self.cache

    def write_cache(self):
        with open("cache.json", "w") as f:
            f.write(self.data.to_json())

    def read_cache(self):
        try:
            with open("cache.json", "r") as f:
                self.cache = f.read()

        except Exception as e:
            print(e)
            with open("cache.json", "w") as f:
                self.cache = self.data.to_json()
                f.write(self.cache)
