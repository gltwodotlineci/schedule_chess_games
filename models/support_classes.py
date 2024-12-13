import random
import json
# method to read json
def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)
    

# method to write json
def write_json(path,list_dict):
    with open(path, 'w') as f:
        json.dump(list_dict, f, indent=2)


def create_id(x=None,y=None,id=None):
    nb_lst = 9
    if x == None:
        nb_lst = 4

    if id == None:
        rand = ''.join([str(random.randint(0,9)) for a in range(1,nb_lst)])
        return rand + x + y

    return id
