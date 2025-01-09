

def correction_dt(data, type):
    '''
    Informing of error in data input
    :param data: dictionary
    :param type: string
    Using type param to inform for the case error and entering the new input
    at the given data
    '''
    if type == 'tournament':
        data_format = "Remember the format of the date:"
        data_format += " 'dd-mm-yyyy and the players must be even' "
        print(data_format)
        data['starting_date'] = input("write again the starting date please: ")
        data['ending_date'] = input("write again the ending date please: ")
        input_text_1 = "write again the number of players please: "
        data['nb_players'] = input(input_text_1)
    elif type == 'round':
        print("Remember the format of the date: 'dd-mm-yyyy-HH:MM' ")
        input_text_2 = "write again the starting date and hour, please: "
        data['starting_date_hour'] = input(input_text_2)
    elif type == 'player':
        data['birth_date'] = input("write again the birthdate please: ")
        print("Remember the fin format example is: 'AB1245' ")
        data['fin'] = input("write again the fin number: ")


def support_create(valid_model, model, data, type):
    '''
    Refactoring the creation fonction for creating all kind of models
    :param valid_model: validate model
    :param model: model
    :param data: dictionary
    :param type: string
    Using validate data to check the input datas, once the data validated
    it create the model
    '''
    try:
        validated_dt = valid_model(**data)
        obj = model(**validated_dt.serialize_validator())
        validate = True
    except ValueError as e:
        print(f"Error: {e}")
        validate = False

    while validate is False:
        correction_dt(data, type)

        try:
            validated_dt = valid_model(**data)
            obj = model(**validated_dt.serialize_validator())
            validate = True
        except ValueError as e:
            print(f"Error: {e}")
            validate = False

    return obj
