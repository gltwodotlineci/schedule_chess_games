

def correction_dt(data, type):
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
        print("Error of date format or of FED ID")
        data['birth_date'] = input("write again the birthdate please: ")
        print("Remember the fin format example is: 'AB1245' ")
        data['fin'] = input("write again the fin number: ")


def support_create(valid_model, model, data, type):
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
