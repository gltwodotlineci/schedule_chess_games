from datetime import datetime
from models.tournament import Tournament
from models.player import Player
from models.round import Round


# Creating rapport model
class Rapport:
    def __init__(self):
        self.date_rapport = datetime.now().strftime("%d-%m-%Y-%H:%M")
        self.list_tournaments = Tournament.all_data()
        self.list_players = Player.all_data()
        self._choosed_tour = {}

    @property
    def choosed_tour(self):
        return self._choosed_tour

    @choosed_tour.setter
    def choosed_tour(self, id):
        tournament = Tournament.from_db(id)
        self._choosed_tour = {
            'tour': tournament,
            'name': tournament.name,
            'starting_date': tournament.starting_date,
            'ending_date': tournament.ending_date,
            'players_list': tournament.players_list,
            'rounds_list': tournament.rounds_list
        }

    @property
    def tour(self):
        return self._choosed_tour.get('tour')

    @property
    def players_list(self):
        players_id_lst = self._choosed_tour.get('players_list')
        players = []
        for player_id in players_id_lst:
            player = Player.from_db('id', player_id)
            players.append(player)

        return players

    @property
    def rounds_lists(self):
        rounds_id_lst = self._choosed_tour.get('rounds_list')
        rounds = []
        for round_id in rounds_id_lst:
            round = Round.from_db(round_id)
            rounds.append(round)

        return rounds
