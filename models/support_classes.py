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


def create_id(id=None,x=None,y=None):
    nb_lst = 9
    if x is not None:
        nb_lst = 4

    if id == None:
        rand = ''.join([str(random.randint(0,9)) for a in range(1,nb_lst)])
        if x is None:
            return rand
        else:
            if y is None:
                return rand + x
            return rand + x.replace(' ','') + y.replace(' ','')
    return id


#select method factorized
def select_from_db(json_path, id):
    list_dt_json = read_json(json_path)
    for element in list_dt_json:
        if element.get('id') == id:
            return element


# Save method factorized
def save_support(json_path, serialized_data,id=None):
    list_dt_json = read_json(json_path)
    if id is None:
        list_dt_json.append(serialized_data)
    else:
        for element in list_dt_json:
            if element.get('id') == id:
                element.update(serialized_data)
                break

    write_json(json_path,list_dt_json)
