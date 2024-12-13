def ask_dt_tournament():
    print("For creating a Tournament please follow the instructions.")
    data = {}
    data['name'] = input("Please write the tournament name: ")
    data['place'] = input("Please write the starting date ")
    data['starting_date'] = input("Please write the ending date ")
    data['ending_date'] = input("Please write your description ")
    return data


