from controller.controller import check_fin
from controller.controller import enter_existing_player
from controller.controller import add_results


def verify_choice(condition, options):
    '''
    Verifying if the given input is consistent with the determined options
    :param condition: string/integer
    :param options: list
    :return: condition input
    '''
    input_var = input(condition)
    while input_var not in options:
        print('Please verify your choice')
        input_var = input(condition)
    return input_var


'''
Menue
'''


def select_or_create():
    # Giving the select choices for the main menu
    print("  ---      You have four choices      ---")
    print("  -- < Add/check the players   - 1 > --")
    print("  -- < Select a tournament     - 2 > --")
    print("  -- < Create a new tournament - 3 > --")
    print("  -- < Create a report        - R > --")

    content = "Please write '1', '2', '3', 'R' or 'C' to close the program "
    return verify_choice(content, ['1', '2', '3', 'R', 'C'])


def go_back():
    # Going back to the main page
    content = "You can go back to the main menu or close the program"
    content += " Please write 'back' or 'C' "
    return verify_choice(content, ['back', 'C'])


'''
Tournament
'''


def send_dt_tourn():
    # Sending details for the tournament
    data = {}
    print("Please enter the data for the tournament")
    data['name'] = input("Please write the tournament name: ")
    data['place'] = input("Please write the place ")
    data['starting_date'] = input("Please write the starting date ")
    data['ending_date'] = input("Please write the ending date ")
    data['description'] = input("Please write your description ")
    print("Before writing how many players will this tournament have")
    print("Remember, your choice must be an even number")
    data['nb_players'] = input("Please write the number of players ")
    int(data['nb_players'])

    return data


def select_tournament(tours):
    '''
    Select one of the tournaments from the list
    :param tours: list of tour objects
    :return: the tour object that fit to the choosed tournament
    '''
    nb_tours = [str(x) for x in range(1, len(tours)+1)]
    content = "For choosing the tournament, write one of the "
    content += f"numbers {' '.join(nb_tours)} "
    nb_tour = verify_choice(content, nb_tours)
    return tours[int(nb_tour)-1]


def nn_complet_tour(tour, missing_pl, missing_rd):
    '''
    Sending to the main page if the choosed tournament has
    missing rounds or players
    :param tour: tour object
    :param missing_pl: integer
    :param missing_rd: integer
    :return: 'back' as string
    '''
    print(f"The tournament {tour.name} is uncompleted")
    print(f"You might need {missing_pl} more players or {missing_rd} rounds")
    cont0 = "In order to complete this tournament go to "
    cont0 += "the option '3' of the main menu"
    print(cont0)
    content = "Please write 'c' to continue to the main menu "
    choice2 = verify_choice(content, ['c'])
    if choice2:
        return 'back'


'''
Players
'''


def ask_add_player():
    # Question part if the user must confirm adding a player
    print("Write 'yes' or 'back' if you want to add a player or to go back")
    content = " Do you want to add a player - 'yes' or 'back' to go back "
    yes_back = verify_choice(content, ['yes', 'back'])
    return yes_back


def send_dt_player():
    '''
    input data for player creation object
    :return: data dictinary with player attributs
    '''
    dt = {}
    print("Please enter the data for the new player")
    given_fin = input("Enter the FED ID ").upper()
    verify_fin = check_fin(given_fin)
    # Check if it already exists on the DB
    while verify_fin is True:
        print("This FED ID already exist. Try another FED ID please ")
        given_fin = input("Enter a non-existent FED ID ").upper()
        verify_fin = check_fin(given_fin)
    dt['fin'] = given_fin
    dt['first_name'] = input("Enter the first name ")
    dt['last_name'] = input("Enter the last name ")
    dt['birth_date'] = input("Enter the birthdate ")
    return dt


# to choose players
def choos_fed_nb(tour, nb):
    '''
    Entering fin (Fed Id) and checking if it is not allredy entered
    in the tournament or if it does exist in the data base
    :param: tour object
    :nb: string
    :return: the fin in uppecase
    '''
    content = f"Enter the player {nb} FED number: "
    given_fin = input(content)
    # if player already exists
    verify_fin = check_fin(given_fin)
    # Verify if there is no dublant
    doublant_check = enter_existing_player(given_fin, tour)

    while verify_fin is False or doublant_check is True:
        print("Check your FED Id choice! Two possible errors.")
        print("   - 1. The FED Id does not exist on your player list")
        print("   - 2. The player is already registered in your tournament")
        given_fin = input(content)
        verify_fin = check_fin(given_fin)
        doublant_check = enter_existing_player(given_fin, tour)

    return given_fin.upper()


'''
Round
'''


# asking if it want to create a round for the new tournament
def create_round_tour(tour_data):
    # Asking if the user want to continue creating rounds for the
    # tournament ent returnin 'yes' or 'back' string
    print("Do you want to start creating a round for the new tournament?")
    rd_4tour = tour_data.round_numbers
    existing_rds = len(tour_data.rounds_list)

    tour_desc = f"Your tournament must have {rd_4tour} rounds,"
    tour_desc += f" and you have {existing_rds} rounds created"
    print(tour_desc)
    content = "Write 'yes' or 'back' if you want to go at"
    content += " the principal menu page "
    return verify_choice(content, ['yes', 'back'])


# asking for date and time
def date_and_time(existing_round):
    # Asking for the datas of the round and sending the data in
    # a dictionary format
    print(" ")
    starting_rnd = "You can start choosing the date and the hour"
    starting_rnd += f" of the Round {existing_round+1}"
    print(starting_rnd)
    end_rnd = f"The ending date-hour of the Round {existing_round+1}"
    end_rnd += "will be filled at the end of the round"
    print(end_rnd)
    form_dat = "Remember, the date-hour format must be like this:"
    form_dat += " 'dd-mm-yyyy-HH:MM'"
    print(form_dat)
    str_dat = "Please enter the date and the hour of the starting date "
    starting_date = input(str_dat)
    data = {
        'starting_date_hour': starting_date,
        'name': f"Round {existing_round+1}",
        'number': existing_round+1
    }
    return data


'''
Game
'''


def choos_winner(players, data_games):
    '''
    Asking user to choos the winner and adding the result to the game
    :param players: list with player objects
    :data_games: dictionary
    :return: list of game objects
    '''
    games = []
    content = "Choose 1 ,2 or 3"
    for i, pl in enumerate(players):
        p1 = f"player1 {pl[0].first_name} {pl[0].last_name} "
        p2 = f"player2 {pl[1].first_name} {pl[1].last_name} "
        print(f"{p1} VS {p2}")
        content = "Choose 1 ,2 or 3 "
        winner = verify_choice(content, ['1', '2', '3'])
        game = add_results(winner, data_games[i])
        games.append(game)

    return games
