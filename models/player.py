from models.support_classes import read_json
from models.support_classes import create_id
from models.support_classes import save_support


class Player:
    def __init__(self, fin, first_name, last_name, birth_date, id=None):
        self.id = create_id(id)
        self.fin = fin
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self._points = None

    def serialize_player(self):
        return {
            'id': str(self.id),
            'fin': self.fin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date
        }

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    @classmethod
    def from_db(cls, key, player_id):
        list_players = read_json('json_data/players.json')
        for player in list_players:
            if player.get(key) == player_id:
                return cls(**player)

    @classmethod
    def all_data(cls):
        lst_players_json = read_json('json_data/players.json')
        players_list = []
        for player in lst_players_json:
            pl = cls(**player)
            players_list.append(pl)

        return players_list

    # save method
    def save_dt(self, id=None):
        save_support("json_data/players.json", self.serialize_player(), id)
