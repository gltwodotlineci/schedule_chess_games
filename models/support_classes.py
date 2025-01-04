import json
import uuid


# method to read json
def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


# method to write json
def write_json(path, list_dict):
    with open(path, 'w') as f:
        json.dump(list_dict, f, indent=2)


# create an uuid
def create_id(id=None):
    if id:
        return id
    return uuid.uuid4()


# select method factorized
def select_from_db(json_path, id):
    list_dt_json = read_json(json_path)

    # generator expression
    match_id = (x for x in list_dt_json if x.get('id') == id)
    # generator
    try:
        obj = next(match_id)
        return obj
    except StopIteration:
        raise ValueError("The given id does not exist")


# Save method factorized
def save_support(json_path, serialized_data):
    list_dt_json = read_json(json_path)
    list_dt_json.append(serialized_data)
    write_json(json_path, list_dt_json)


# Update method factorized
def update_support(json_path, serialized_data, id):
    lst_dt_json = read_json(json_path)
    # generator expression
    match_id = (x for x in lst_dt_json if x.get('id') == id)
    # generator
    try:
        obj = next(match_id)
        obj.update(serialized_data)
        write_json(json_path, lst_dt_json)
    except StopIteration:
        raise ValueError("The given id does not exist")
