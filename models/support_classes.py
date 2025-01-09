import json
import uuid


# method to read json
def read_json(path):
    '''
    It will search the file based on the path
    :param path: Given json path
    return json data
    '''
    with open(path, 'r') as f:
        return json.load(f)


# method to write json
def write_json(path, list_dict):
    '''
    It will search the file based on the path and
    :param path: given json path
    :param list_dict: dictionary
    Save the of the dictionary in the json path document
    '''
    with open(path, 'w') as f:
        json.dump(list_dict, f, indent=2)


# create an uuid
def create_id(id=None):
    '''
    Creating an uuid as object id
    :param id: uuid/None
    return an existing uuid if id not None. If not creating and returning it
    '''
    if id:
        return id
    return uuid.uuid4()


# select method factorized
def select_from_db(json_path, id):
    '''
    Using generator to send a choosed object as dictionary
    :param json_path: given json path
    :param id: uuid
    return dictionary object based on the given id
    '''
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
    '''
    Saving given data at given json path
    :param json_path: given json path
    :param serilized_data: data serialized as dictionary
    '''
    list_dt_json = read_json(json_path)
    list_dt_json.append(serialized_data)
    write_json(json_path, list_dt_json)


# Update method factorized
def update_support(json_path, serialized_data, id):
    '''
    Updating given data choosed from its id at given json path
    :param json_path: given json path
    :param serilized_data: data serialized as dictionary
    :param id: uuid
    '''
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
