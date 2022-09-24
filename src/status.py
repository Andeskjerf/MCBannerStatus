from mcstatus import JavaServer

from src.data_cache import DataCache


class Status:

    data: DataCache = DataCache(0, 0, None, False)
    cache: str = None
    updated = False

    host: str
    port: int

    online_text: str
    offline_text: str
    player_failed_text: str

    def __init__(
            self,
            host,
            port,
            online_text,
            offline_text,
            player_failed_text
    ):
        self.host = host
        self.port = port
        self.online_text = online_text
        self.offline_text = offline_text
        self.player_failed_text = player_failed_text
        self.read_cache()

        try:
            status = JavaServer(self.host, self.port).status()
            self.data.online_players = status.players.online
            self.data.max_players = status.players.max
            self.data.version = status.version.name
            self.data.active = True

        except Exception as e:
            print(e)
            self.data.online_players = 0
            self.data.max_players = 0
            self.data.active = False

        self.updated = self.has_changed()
        if self.updated:
            self.write_cache()

    def get_player_count(self):
        if not self.data.active:
            return self.player_failed_text
        return f"{self.data.online_players} / {self.data.max_players}"

    def get_status(self):
        if not self.data.active:
            return self.offline_text
        return self.online_text

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
