from models.support_classes import read_json
from models.support_classes import write_json
from models.support_classes import create_id

class Tournament:
    def __init__(
            self,
            name,
            place,
            starting_date,
            ending_date,
            description,
            id = None,
            rounds_list = [],
            players_list = [],
            round_numbers = 4,
            actual_round_number = 0
            ):
        self.id = create_id(name)
        self.name = name
        self.place = place
        self.starting_date = starting_date      
        self.ending_date = ending_date
        self.description = description
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.round_numbers = round_numbers
        self.actual_round_number = actual_round_number


    def serialize_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'place': self.place,
            'starting_date': self.starting_date,
            'ending_date': self.ending_date,
            'description': self.description,
            'rounds_list': self.rounds_list,
            'players_list': self.players_list,
            'round_numbers': self.round_numbers,
            'actual_round_number': self.actual_round_number
        }


    @classmethod
    def from_db(cls, id):
        list_tours = read_json('json_data/tournaments.json')
        for tour in list_tours:
            if tour.get("id") == id:
                return cls(**tour)
            

    @classmethod
    def all_data(cls):
        lst_tours_json = read_json('json_data/tournaments.json')
        tournaments_list = []
        for tournament in lst_tours_json:
            tr = cls(**tournament)
            tournaments_list.append(tr)

        return tournaments_list

    # save:
    def save(self,id=None):
        lst_tours_json = read_json('json_data/tournaments.json')
        for tournament in lst_tours_json:
            if tournament.get('id') == id:
                tournament.update(self.serialize_data())
                break

        lst_tours_json.append(self.serialize_data())
        write_json('json_data/tournaments.json', lst_tours_json)       
