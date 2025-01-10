from datetime import datetime
from models.tournament import Tournament
from models.player import Player
from models.round import Round


# Creating report model
class Report:
    '''
    The class handles report initialization, input processing,
    rendering report and object mining.

    Attributes:
        date_report uuid:
        list_tournaments list:
        list_players list:
        choosed_tou dictionary:

    Methods:
        __init__(): Initializing class.
        choosed_tour(getter=True): Getter of choosed_tour where we have the
                    tournaments values in a dictionary format.
        choosed_tour(id): Setter of choosed_tour and by population it.
        tour(getter=True): Getter of the tour object.
        players_list(): Getter of player objects in a list.
        rounds_lists(): Getter of round objects in a list.
    '''
    def __init__(self):
        self.date_report = datetime.now().strftime("%d-%m-%Y-%H:%M")
        self.list_tournaments = Tournament.all_data()
        self.list_players = Player.all_data()
        self._choosed_tour = {}

    @property
    def choosed_tour(self):
        '''
        It will return the choosed tournament
        :param choosed_tour: dictionary with tournament data.
        :return: A dictionary with the keys and their respectiv values.
        tour, name, starting_date, ending_date, players_list and rounds_list
        '''
        return self._choosed_tour

    @choosed_tour.setter
    def choosed_tour(self, id):
        '''
        It will set the value of the choosed tour instance
        :param id: given uuid
        The uuid value will be used to get a tournament and populate
        the choosed_tour
        '''
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
        '''
        It will return the tournament
        :param tour: uuid.
        :return: The uuid of a tournament
        '''
        return self._choosed_tour.get('tour')

    @property
    def players_list(self):
        '''
        It will return the players list
        :param players_list: list.
        :return: A list of players uuid
        '''
        players_id_lst = self._choosed_tour.get('players_list')
        players = []
        for player_id in players_id_lst:
            player = Player.from_db('id', player_id)
            players.append(player)

        return players

    @property
    def rounds_lists(self):
        '''
        It will return the rounds list
        :param rounds_list: list.
        :return: A list of rounds uuid
        '''
        rounds_id_lst = self._choosed_tour.get('rounds_list')
        rounds = []
        for round_id in rounds_id_lst:
            round = Round.from_db(round_id)
            rounds.append(round)

        return rounds
