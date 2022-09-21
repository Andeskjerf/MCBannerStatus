import re
from mcrcon import MCRcon
from .conf import MCRCON_HOST, MCRCON_PASSWORD, MCRCON_PORT


class Status:

    max_players: int = 0
    online_players: int = 0
    active: bool = False

    def __init__(self):
        try:
            with MCRcon(MCRCON_HOST, MCRCON_PASSWORD, port=MCRCON_PORT) as mcr:
                res = mcr.command("list").splitlines(keepends=False)
                nums = re.findall(r"[0-9]+", res[0])

                if len(nums) == 2:
                    self.online_players = int(nums[0])
                    self.max_players = int(nums[1])
                    self.active = True
                else:
                    raise Exception("Could not parse player count")
        except:
            self.active = False


    def get_player_count(self):
        if not self.active:
            return "Unable to establish connection"
        return f"{self.online_players} / {self.max_players}"


    def get_status(self):
        if not self.active:
            return "Offline"
        return "Online"
