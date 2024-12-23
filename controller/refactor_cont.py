from models.tournament import Tournament
from controller.validator import ValidateTournament


def correction_dt(data,type):
    if type == 'tournament':
        print("Remember the format of the date: 'dd-mm-yyyy and the players must be even' ")
        data['starting_date'] = input("write again the starting date please: ")
        data['ending_date'] = input("write again the ending date please: ")
        data['nb_players'] = input("write again the number of players please: ")
    elif type == 'round':
        print("Remember the format of the date: 'dd-mm-yyyy-HH:MM' ")
        data['starting_date_hour'] = input("write again the starting date and hour please: ")
    elif type == 'player':
        print("Error of date format or of FED ID")
        data['birth_date'] = input("write again the birth date please: ")
        print("Remember the fin format exemple is: 'AB1245' ")
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
