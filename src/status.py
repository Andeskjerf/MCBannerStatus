from mcstatus import JavaServer

from src.data_cache import Cacher, DataCache


class Status:

    data: DataCache = None
    cache: Cacher = None

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

        self.data = self.cache.data

        try:
            status = JavaServer(self.host, self.port).status()
            self.cache.update(
                **{
                    "max_players": status.players.max,
                    "online_players": status.players.online,
                    "version": status.version.name,
                    "active": True
                }
            )

        except Exception as e:
            print(e)
            self.cache.update(
                **{
                    "max_players": 0,
                    "online_players": 0,
                    "active": False
                }
            )

    def get_player_count(self):
        if not self.data.active:
            return self.player_failed_text
        return f"{self.data.online_players} / {self.data.max_players}"

    def get_status(self):
        if not self.data.active:
            return self.offline_text
        return self.online_text
