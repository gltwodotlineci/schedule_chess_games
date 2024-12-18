from models.support_classes import read_json
from models.support_classes import create_id
from models.support_classes import select_from_db
from models.support_classes import save_support

class Tournament:
    def __init__(
            self,
            name,
            place,
            starting_date,
            ending_date,
            description,
            nb_players,
            id = None,
            rounds_list = [],
            players_list = [],
            round_numbers = 4,
            actual_round_number = 0
            ):
        self.id = create_id(id)
        self.name = name
        self.place = place
        self.starting_date = starting_date      
        self.ending_date = ending_date
        self.description = description
        self.nb_players = nb_players
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.round_numbers = round_numbers
        self.actual_round_number = actual_round_number


    def serialize_data(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'place': self.place,
            'starting_date': self.starting_date,
            'ending_date': self.ending_date,
            'nb_players': self.nb_players,
            'description': self.description,
            'rounds_list': self.rounds_list,
            'players_list': self.players_list,
            'round_numbers': self.round_numbers,
            'actual_round_number': self.actual_round_number
        }
    


    @classmethod
    def from_db(cls, id):
        tournament = select_from_db("json_data/tournaments.json",id)
        return cls(**tournament)


    @classmethod
    def all_data(cls):
        lst_tours_json = read_json('json_data/tournaments.json')
        tournaments_list = []
        for tournament in lst_tours_json:
            tr = cls(**tournament)
            tournaments_list.append(tr)

        return tournaments_list


    # save  method
    def save(self,id=None):
        #factoried save function
        save_support("json_data/tournaments.json", self.serialize_data(),id)
