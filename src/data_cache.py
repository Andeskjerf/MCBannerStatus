import json


class DataCache:

    max_players: int = 0
    online_players: int = 0
    version: str = None
    active: bool = False

    def __init__(self, max_players, online_players, version, active):
        self.max_players = max_players
        self.online_players = online_players
        self.version = version
        self.active = active

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
