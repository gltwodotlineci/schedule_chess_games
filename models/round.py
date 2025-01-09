from models.support_classes import read_json
from models.support_classes import save_support
from models.support_classes import select_from_db
from models.support_classes import create_id
from models.support_classes import update_support


class Round:
    def __init__(
            self,
            tournament_id,
            name,
            number,
            starting_date_hour,
            ending_date_hour=None,
            id=None,
            games_list=[]
            ):
        self.id = create_id(id)
        self.tournament_id = tournament_id
        self.name = name
        self.number = number
        self.starting_date_hour = starting_date_hour
        self.ending_date_hour = ending_date_hour
        self.games_list = games_list

    def serialize_data(self):
        '''
        Serializing a round object.
        :return: round object as dictionary with the keys and theri
        respective values as: id, tournament_id, number, games_list
        and ending_date_hour
        '''
        return {
            'id': str(self.id),
            'tournament_id': self.tournament_id,
            'name': self.name,
            'number': self.number,
            'starting_date_hour': self.starting_date_hour,
            'games_list': self.games_list,
            'ending_date_hour': self.ending_date_hour
        }

    # geting obj
    @classmethod
    def from_db(cls, id):
        '''
        Using a class method to send json data as object selected from
        the given id
        :param id: uuid of a specific round
        :return: a round object based on the given id
        '''
        round = select_from_db("json_data/rounds.json", id)
        return cls(**round)

    # send all data method
    @classmethod
    def all_data(cls):
        '''
        Using a class method to send all json rounds data  as objects
        :return: A list of all round objects
        '''
        list_rounds_jsn = read_json("json_data/rounds.json")
        rounds_list = []
        for round in list_rounds_jsn:
            rnd = cls(**round)
            rounds_list.append(rnd)

        return rounds_list

    # save method
    def save(self):
        # saving the game object on games.json
        save_support("json_data/rounds.json", self.serialize_data())

    # update method
    def update(self, id):
        '''
        Updating a round object at json_data
        :param id: uuid of a choosen round
        It will use the id to update a round object and
        save the changes on rounds.json
        '''
        update_support("json_data/rounds.json", self.serialize_data(), id)
