import json
import uuid

# method to read json
def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)
    

# method to write json
def write_json(path,list_dict):
    with open(path, 'w') as f:
        json.dump(list_dict, f, indent=2)

# create an uuid
def create_id(id=None):
    if id:
        return id
    return uuid.uuid4()


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
