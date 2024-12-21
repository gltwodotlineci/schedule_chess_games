from models.support_classes import read_json
from models.support_classes import save_support
from models.support_classes import select_from_db
from models.support_classes import create_id



class Game():
    def __init__(self,round_id, player1, player2, round_nb, res_p1=None, res_p2=None, id=None):
        self.id = create_id(id)
        self.round_id = round_id
        self.player1_result = [player1, res_p1]
        self.player2_result = [player2, res_p2]
        self.round_nb = round_nb


    @property
    def player1(self):
        return self.player1_result[0]


    @property
    def player2(self):
        return self.player2_result[0]
    
    @property
    def res_p1(self):
        return self.player1_result[1]
    
    @property
    def res_p2(self):
        return self.player2_result[1]


    def set_winner(self, winner):
        if winner == self.player1:
            self.player1_result[1] = True
        elif winner == self.player2:
            self.player2_result[1] = True
        elif winner == "None":
            self.player1_result[1] = False
            self.player2_result[1] = False

        
    def serialize_data(self):
        return {
            'id': str(self.id),
            'round_id': self.round_id,
            'player1_result': self.player1_result,
            'player2_result': self.player2_result,
            'round_nb': self.round_nb
        }


    @classmethod
    def from_db(cls,id):
        game = select_from_db("json_data/games.json",id)
        data={
            'id':game.get('id'),
            'round_id': game.get('round_id'),
            'player1': game.get('player1_result')[0],
            'player2': game.get('player2_result')[0],
            'round_nb': game.get('round_nb'),
            'res_p1': game.get('player1_result')[1],
            'res_p2': game.get('player2_result')[1]
        }
        return cls(**data)

    # send all data method
    @classmethod
    def all_data(cls):
        list_games_json = read_json("json_data/games.json")
        games_list = []
        for game in list_games_json:
            data={
            'id':game.get('id'),
            'round_id': game.get('round_id'),
            'player1': game.get('player1_result')[0],
            'player2': game.get('player2_result')[0],
            'round_nb': game.get('round_nb'),
            'res_p1': game.get('player1_result')[1],
            'res_p2': game.get('player2_result')[1]

            }

            gm = cls(**data)
            games_list.append(gm)

        return games_list


    #save method
    def save(self, id=None):       
        save_support("json_data/games.json", self.serialize_data(),id)
