from models.support_classes import read_json
from models.support_classes import create_id
from models.support_classes import select_from_db
from models.support_classes import save_support
from models.support_classes import update_support


class Tournament:
    '''
    The class handles tournament initialization, input processing,
    state updates, rendering and managing the round state and rational data.

    Attributes:
        id uuid: To identify the tournament
        name string: The tournament's name.
        place string: Place of the tournament.
        starting_date date string: The date of starting tounrnament.
        ending_date date string: The date of ending tournament.
        description string: description.
        nb_players string: The number of players for the tournament.
        rounds_list list with uuid: list of rounds in the tournament.
        players_list list with uuid: list of players in the tournament.
        round_numbers string: The total number of round for tournament.
        actual_round_number integer: The round in progress.

    Methods:
        __init__(name, place, starting_date, ending_date, description,
            nb_players, rounds_list, players_list, round_number,
            actual_round_number, id) Initializing class with the
            given parameters.
        serialize_data(): Serialize tournament data in dictionary format.
        from_db(cls, id): specific tournament object according to given id.
        all_data(cls): Returning all tournaments objects in a list.
        save(): Saving the tournament object on tournaments.json
        update(id): Update tournament object with the given id on
                   tournaments.json
        last_tour(cls): Giving the last created tournament object.
    '''
    def __init__(
            self,
            name,
            place,
            starting_date,
            ending_date,
            description,
            nb_players,
            id=None,
            rounds_list=[],
            players_list=[],
            round_numbers=4,
            actual_round_number=0
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
        '''
        Serializing a tournament object.
        :return: tournament object as dictionary with the keys and their
        respective values as: id, name, place, starting_date, ending_date
        description, nb_players, rounds_players, players_list, round_numbers
        and actual_round_number
        '''
        return {
            'id': str(self.id),
            'name': self.name,
            'place': self.place,
            'starting_date': self.starting_date,
            'ending_date': self.ending_date,
            'description': self.description,
            'nb_players': self.nb_players,
            'rounds_list': self.rounds_list,
            'players_list': self.players_list,
            'round_numbers': self.round_numbers,
            'actual_round_number': self.actual_round_number
        }

    @classmethod
    def from_db(cls, id):
        '''
        Using a class method to send json data as object selected from
        the given id
        :param id: uuid of a specific tournament
        :return: a tournament object based on the given id
        '''
        tournament = select_from_db("json_data/tournaments.json", id)
        return cls(**tournament)

    @classmethod
    def all_data(cls):
        '''
        Using a class method to send all json tournament data  as objects
        :return: A list of all tournament objects
        '''
        lst_tours_json = read_json('json_data/tournaments.json')
        tournaments_list = []
        for tournament in lst_tours_json:
            tr = cls(**tournament)
            tournaments_list.append(tr)

        return tournaments_list

    # save  method
    def save(self):
        # factoried save function
        save_support("json_data/tournaments.json", self.serialize_data())

    # update method
    def update(self, id):
        '''
        Updating a tournament object at json_data
        :param id: uuid of a choosen tournament
        It will use the id to update a tournament object and
        save the changes on tournaments.json
        '''
        update_support("json_data/tournaments.json", self.serialize_data(), id)

    # giving last touranement
    @classmethod
    def last_tour(cls):
        '''
        Using class method so we can send the last tournament object
        '''
        all_tours_json = read_json('json_data/tournaments.json')
        nb_last = len(all_tours_json)
        if nb_last == 0:
            return False
        last_tour_json = all_tours_json[nb_last-1]
        last_tour = cls(**last_tour_json)
        return last_tour
