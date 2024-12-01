import random
def create_id(x):
    rand = ''.join([str(random.randint(0,9))for a in range(1,4)])
    return rand + x
class Tournament:
    def __init__(
            self,
            name,
            starting_date,
            ending_date,
            description,
            rounds_list = None,
            players_list = None,
            round_numbers = 4,
            actual_round_number = 1
            ):
        self.id = create_id(self.name)
        self.name = name
        self.starting_date = starting_date      
        self.ending_date = ending_date
        self.round_numbers = 4
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.description = description
        self.round_numbers = round_numbers
        self.actual_round_number = actual_round_number
