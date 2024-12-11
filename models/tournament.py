import random
import json

# method to read json
def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


# method to write json
def write_json(path,list_dict):
    with open(path, 'w') as f:
        json.dump(list_dict, f, indent=2)

def create_id(x):
    rand = ''.join([str(random.randint(0,9))for a in range(1,4)])
    return rand + x.replace(' ','_')
class Tournament:
    def __init__(
            self,
            name,
            place,
            starting_date,
            ending_date,
            description,
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
        self.round_numbers = 4
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.description = description
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
    def from_db(cls, tour_id):
        list_tours = read_json('json_data/tournaments.json')
        for tour in list_tours:
            if tour.get("id") == tour_id:
                return cls(**tour)

    # save:
    def save(self):
        pass
