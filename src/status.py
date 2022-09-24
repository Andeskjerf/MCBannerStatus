from mcstatus import JavaServer

from src.data_cache import DataCache


class Status:

    cache: DataCache = None

    host: str
    port: int

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

        try:
            status = JavaServer(self.host, self.port).status()
            self.cache.max_players = status.players.max
            self.cache.online_players = status.players.online
            self.cache.description = status.description
            self.cache.favicon = status.favicon
            self.cache.version = status.version.name
            self.cache.active = True

        except Exception as e:
            print(e)
            self.cache.max_players = 0
            self.cache.online_players = 0
            self.cache.active = False

    def get_player_count(self):
        if not self.cache.active:
            return self.player_failed_text
        return f"{self.cache.online_players} / {self.cache.max_players}"

    def get_status(self):
        if not self.cache.active:
            return self.offline_text
        return self.online_text
