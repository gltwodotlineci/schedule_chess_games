from models.support_classes import read_json
from models.support_classes import save_support
from models.support_classes import select_from_db
from models.support_classes import create_id
from models.support_classes import update_support
import random


class Game():
    '''
    The class handles game initialization, input processing, state updates,
    rendering and managing the result of the game and which player
    will start the game. also handeling rational data.

    Attributes:
        id uuid: To identify the game
        round_id uuid: foreign key of the round that the game belongs
        player1 uuid: The player's id that will play as the first player
        player2 uuid: The player's id that will play as the second player
        res_p1 boolean: True if the player 1 has won, Draw if it's a draw.
        res_p2 boolean: True if the player 2 has won, Draw if it's a draw.
        white_king uuid: The uuid of player 1 or 2

    Methods:
        __init__(round_id, palayer1, player2, res_p1, res_p2, white_king, id):
                        Initializing class with the given parameters.
        serialize_data(): Serialize data in dictionary format
        player1(getter=True): Getter of player1.
        player2(getter=True): Getter of player2.
        res_p1(getter=True): Getter of result of player1.
        res_p2(getter=True): Getter of result of player2.
        white_king(getter=True): Getter of player's uuid that will
                                be the white king.
        white_king(value): Setter of the white king. Associating uuid
                            of the player that will be white king

        set_winner(winner): Will set the player_result to win or False
        from_db(cls, id): specific game object according to given id
        all_data(cls): Returning all game objects in a list
        save(): Saving the game object on games.json
        update(id): Update game object with the given id on games.json
        filter_by_instance(instance, name): Filter one or multiple json_data
                                            based on the given value
    '''
    def __init__(
            self,
            round_id,
            player1,
            player2,
            res_p1=None,
            res_p2=None,
            white_king=None,
            id=None
            ):
        self.id = create_id(id)
        self.round_id = round_id
        self.player1_result = [player1, res_p1]
        self.player2_result = [player2, res_p2]
        players = [player1, player2]
        self._white_king = players[random.randint(0, 1)]

    def serialize_data(self):
        '''
        Serializing a game object.
        :return: game object as dictionary with the keys and their
        respective values as: id, player1_result, player2_result
        and white_king
        '''
        return {
            'id': str(self.id),
            'round_id': self.round_id,
            'player1_result': self.player1_result,
            'player2_result': self.player2_result,
            'white_king': self.white_king
        }

    @property
    def player1(self):
        '''
        It will return the value player1
        :param player1: uuid of player1
        :return: the uuid of player1
        '''
        return self.player1_result[0]

    @property
    def player2(self):
        '''
        It will return the value player2
        :param player1: uuid of player2
        :return: the uuid of player2
        '''
        return self.player2_result[0]

    @property
    def res_p1(self):
        '''
        It will return the result of player1
        :param res_p1: Result of res_p1
        :return: True or False
        '''
        return self.player1_result[1]

    @property
    def res_p2(self):
        '''
        It will return the result of player2
        :param res_p1: Result of res_p2
        :return: True or False
        '''
        return self.player2_result[1]

    @property
    def white_king(self):
        '''
        It will return the player that is white king
        :param _white_king: uuid of player1 or player2
        :return: uuid of white king player
        '''
        return self._white_king

    @white_king.setter
    def white_king(self, value):
        '''
        It will set the value of the white king
        :param value: given uuid
        The uuid value will be passed at the white_king instance
        '''
        self._white_king = value

    def set_winner(self, winner):
        '''
        Seting the winner to the player
        :param winner: uuid of the winner
        The player1_result[1], or the player2_reslut[2] will have the
        value True if winner correspond to it's uuid, of False if not
        '''
        if winner == self.player1:
            self.player1_result[1] = True
        elif winner == self.player2:
            self.player2_result[1] = True
        elif winner == "None":
            self.player1_result[1] = False
            self.player2_result[1] = False

    @classmethod
    def from_db(cls, id):
        '''
        Using a class method to send json data as object selected from
        the given id
        :param id: uuid of a specific game
        :return: a game object based on the given id
        '''
        game = select_from_db("json_data/games.json", id)
        data = {
            'id': game.get('id'),
            'round_id': game.get('round_id'),
            'player1': game.get('player1_result')[0],
            'player2': game.get('player2_result')[0],
            'white_king': game.get('white_king'),
            'res_p1': game.get('player1_result')[1],
            'res_p2': game.get('player2_result')[1]
        }
        return cls(**data)

    # send all data method
    @classmethod
    def all_data(cls):
        '''
        Using a class method to send all json games data  as objects
        :return: A list of all game objects
        '''
        list_games_json = read_json("json_data/games.json")
        games_list = []
        for game in list_games_json:
            data = {
                'id': game.get('id'),
                'round_id': game.get('round_id'),
                'player1': game.get('player1_result')[0],
                'player2': game.get('player2_result')[0],
                'white_king': game.get('white_king'),
                'res_p1': game.get('player1_result')[1],
                'res_p2': game.get('player2_result')[1]
            }
            gm = cls(**data)
            games_list.append(gm)

        return games_list

    # save method
    def save(self):
        save_support("json_data/games.json", self.serialize_data())

    # update method
    def update(self, id):
        '''
        Updating a game object at json_data
        :param id: uuid of a choosen game
        It will use the id to update a game object and
        save the changes on games.json
        '''
        update_support("json_data/games.json", self.serialize_data(), id)

    # filter method
    @classmethod
    def filter_by_instance(cls, instance, name):
        '''
        Filter one or miltiple json_data based on the given value
        :param instance: the instance that we want to use for selection
        :param name: the value of the instance that we want to select
        :return: a list of game/games filtered based on the name (id)
        '''
        list_games_json = read_json("json_data/games.json")
        games = []
        for game in list_games_json:
            if game.get(instance) == name:
                data = {
                    'id': game.get('id'),
                    'round_id': game.get('round_id'),
                    'player1': game.get('player1_result')[0],
                    'player2': game.get('player2_result')[0],
                    'white_king': game.get('white_king'),
                    'res_p1': game.get('player1_result')[1],
                    'res_p2': game.get('player2_result')[1]
                }
                gm = cls(**data)
                games.append(gm)

        return games
