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
        last_update=None
    ):
        self.max_players = max_players
        self.online_players = online_players
        self.version = version
        self.active = active
        self.last_update = last_update

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
