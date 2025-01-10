from models.support_classes import read_json
from models.support_classes import create_id
from models.support_classes import save_support


class Player:
    '''
    The class handles player initialization, input processing,
    rendering and managing the points instance.

    Attributes:
        id uuid: To identify the player
        fin string: Federation identification number.
        first_name string: Player's first name.
        last_name string: Player's last name.
        birth_date date string: Player's birthdate.
        points integer: Instance with player points for a given tournament.

    Methods:
        __init__(fin, first_name, last_name, birth_date, id):
                            Initializing class with the given parameters.
        serialize_player(): Serialize data in dictionary format
        points(getter=True): Getter of points.
        points(value): Setter of points with the giving value.
        from_db(cls, id): Return specific player object according to given id
        all_data(cls): Return all player objects in a list
        save(): Saving the player object on players.json


    '''
    def __init__(self, fin, first_name, last_name, birth_date, id=None):
        self.id = create_id(id)
        self.fin = fin
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self._points = None

    def serialize_player(self):
        return {
            'id': str(self.id),
            'fin': self.fin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date
        }

    @property
    def points(self):
        '''
        It will return the points of the player
        :param points: integer
        :return: commulated points
        '''
        return self._points

    @points.setter
    def points(self, value):
        '''
        It will set the value of players point
        :param value: integer
        The value will pe passed to points instance
        '''
        self._points = value

    @classmethod
    def from_db(cls, key, player_id):
        '''
        Using a class method to send json data as object selected from
        the given id
        :param key: the instance name
        :param player_id: uuid of a specific player
        :return: a player objedct based on the given instance and the id
        '''
        list_players = read_json('json_data/players.json')

        # generator expression
        match_id = (pl for pl in list_players if pl.get(key) == player_id)
        # generator
        try:
            player = next(match_id)
            return cls(**player)
        except StopIteration:
            raise ValueError("The given id does not exist")

    @classmethod
    def all_data(cls):
        '''
        Using a class method to send all json players data  as objects
        :return: A list of all players objects
        '''
        lst_players_json = read_json('json_data/players.json')
        players_list = []
        for player in lst_players_json:
            pl = cls(**player)
            players_list.append(pl)

        return players_list

    # save method
    def save(self):
        # saving the player object on players.json
        save_support("json_data/players.json", self.serialize_player())
