import re
from mcstatus import JavaServer

from src.data_cache import DataCache


class Status:

    cache: DataCache

    host: str
    port: int

    server: JavaServer

    online_text: str
    offline_text: str
    player_failed_text: str

    def __init__(
            self,
            cache,
            host,
            port,
            online_text,
            offline_text,
            player_failed_text
    ):
        self.cache = cache
        self.host = host
        self.port = port
        self.online_text = online_text
        self.offline_text = offline_text
        self.player_failed_text = player_failed_text

        self.server = JavaServer(self.host, self.port)

    def fetch_status(self):
        try:
            status = self.server.status()
            self.cache.max_players = status.players.max
            self.cache.online_players = status.players.online
            self.parse_description(status.description)
            self.cache.favicon = status.favicon.replace("data:image/png;base64,", "")
            self.cache.version = status.version.name
            self.cache.active = True

        except Exception as e:
            print(e)
            self.cache.max_players = 0
            self.cache.online_players = 0
            self.cache.active = False

    # Split server MOTD by newline
    # First line will be server name, second will act as the MOTD
    def parse_description(self, desc) -> str:
        split = desc.split("\n")
        name = split[0]
        motd = split[1]

        # Strip formatting codes
        self.cache.name = re.sub(r"§+.", "", name)
        self.cache.motd = re.sub(r"§+.", "", motd)

    def get_player_count(self):
        if not self.cache.active:
            return self.player_failed_text
        return f"{self.cache.online_players} / {self.cache.max_players}"

    def get_status(self):
        if not self.cache.active:
            return self.offline_text
        return self.online_text
