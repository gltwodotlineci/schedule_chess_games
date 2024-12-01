

class Tournament:
    def __init__(
            self,
            name,
            starting_date,
            ending_date,
            actual_round_number,
            rounds_list,
            players_list,
            description
            ):
        self.name = name
        self.starting_date = starting_date      
        self.ending_date = ending_date
        self.round_number = 4
        self.actual_round_number = actual_round_number
        self.rounds_list = rounds_list
        self.players_list = players_list
        self.description = description
