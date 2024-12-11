
class Round:
    def __init__(
            self,
            tournament_id,
            name,
            number,
            starting_date_hour = None,
            ending_date_hour = None
            ):

        self.tournament_id = tournament_id
        self.name = name
        self.number = number
        self.starting_date_hour = starting_date_hour
        self.ending_date_hour = ending_date_hour
        self.games_list = []

    def serialize_round(self):
        return {
            'tournement_id': self.tournament_id,
            'name': self.name,
            'number': self.number,
            'game_list': self.games_list,
            'starting_date_hour': self.starting_date_hour,
            'ending_date_hour': self.ending_date_hour
        }
