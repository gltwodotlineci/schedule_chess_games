from models.support_classes import read_json
from models.support_classes import write_json
from models.support_classes import create_id

class Player:
    def __init__(self,fin, first_name, last_name, birth_date,id = None, points=0.0):
        self.fin = fin
        self.id = create_id(first_name, last_name, id)
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.points = points


    def serialize_player(self):
        return {
            'id': self.id,
            'fin': self.fin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'points': self.points
        }
    

    @classmethod
    def from_db(cls, player_id):
        list_players = read_json('json_data/players.json')
        for player in list_players:
            if player.get('id') == player_id:
                return cls(**player)

    
    @classmethod
    def all_data(cls):
        lst_players_json = read_json('json_data/players.json')
        players_list = []
        for player in lst_players_json:
            pl = cls(**player)
            players_list.append(pl)

        return players_list


    def save_dt(self, id=None):
        lst_players_json = read_json('json_data/players.json')
        for player in lst_players_json:
            if player.get('id') == id:
                player.update(self.serialize_player())# = self.serialize_player()
                break

        lst_players_json.append(self.serialize_player())
        write_json('json_data/players.json',lst_players_json)
