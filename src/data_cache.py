from datetime import datetime
import json


class DataCache:

    max_players: int = 0
    online_players: int = 0
    version: str = None
    active: bool = False
    last_update: datetime = None

    def __init__(
        self,
        max_players,
        online_players,
        version,
        active,
        last_update=datetime.now()
    ):
        self.max_players = max_players
        self.online_players = online_players
        self.version = version
        self.active = active
        self.last_update = last_update

    def to_json(self):
        return json.dumps(self, default=self.json_default)

    def json_default(self, obj):
        if isinstance(obj, datetime):
            return obj.timestamp()
        else:
            return obj.__dict__


class Cacher:

    data: DataCache = DataCache(0, 0, None, False)
    cache: str = None

    def __init__(self) -> None:
        self.read_cache()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self.data, k, v)

    def has_changed(self):
        cache_dict: dict = json.loads(self.cache)
        data_dict: dict = json.loads(self.data.to_json())
        cache_dict.pop("last_update")
        data_dict.pop("last_update")
        return data_dict != cache_dict

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
