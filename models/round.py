from models.support_classes import read_json
from models.support_classes import save_support
from models.support_classes import select_from_db
from models.support_classes import create_id


class Round:
    def __init__(
            self,
            tournament_id,
            name,
            number,
            starting_date_hour,
            ending_date_hour = None,
            id = None,
            games_list = []
            ):
        self.id = create_id(id)
        self.tournament_id = tournament_id
        self.name = name
        self.number = number
        self.starting_date_hour = starting_date_hour
        self.ending_date_hour = ending_date_hour
        self.games_list = games_list

    def serialize_data(self):
        return {
            'id': str(self.id),
            'tournament_id': self.tournament_id,
            'name': self.name,
            'number': self.number,
            'games_list': self.games_list,
            'starting_date_hour': self.starting_date_hour,
            'ending_date_hour': self.ending_date_hour
        }


    #geting obj
    @classmethod
    def from_db(cls, id):
        round = select_from_db("json_data/rounds.json", id)
        return cls(**round)
            

    # send all data method
    @classmethod
    def all_data(cls):
        list_rounds_jsn = read_json("json_data/rounds.json")
        rounds_list = []
        for round in list_rounds_jsn:
            rnd = cls(**round)
            rounds_list.append(rnd)

        return rounds_list


    #save method
    def save(self, id=None):
        save_support("json_data/rounds.json", self.serialize_data(),id)
