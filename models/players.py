import random
def create_id(x,y):
    rand =''.join([str(random.randint(0,9)) for a in range(1,4)])
    return rand + x + y

class Player:
    def __init__(self, first_name, last_name, birth_date,points=0.0):
        self.id = create_id(first_name, last_name)
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.points = points

    def serialize_players(self):
        return {   
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'points': self.points
        }
    
    
