from models.player import Player

def verify_choice(condition,options):
    input_var = input(condition)
    while input_var not in options:
        print(f'Please verify your choice')
        input_var = input(condition)
    return input_var


def send_dt_tourn():
    data = {}
    print("Please enter the data for the tournament")
    data['name'] = input("Please write the tournament name: ")
    data['place'] = input("Please write the place ")
    data['starting_date'] = input("Please write the starting date ")
    data['ending_date'] = input("Please write the ending date ")
    data['description'] = input("Please write your description ")
    return data 

# Players
def ask_add_player():
    print("Write 'yes' or 'back' if you want to add a player or to go back")
    content = " Do you want to add a playe - 'yes' or to go back 'back' "
    yes_back = verify_choice(content,['yes', 'back'])
    return yes_back

def send_dt_player():
    dt = {}
    print("Please enter the data for the new player")
    dt['fin'] = input("Enter the FID ID ").upper()
    dt['first_name'] = input("Enter the first name ")
    dt['last_name'] = input("Enter the last name ")
    dt['birth_date'] = input("Enter the birth date ")
    return dt


def send_dt_round():
    dt = []
    print("Please enter the data for the round ")
    print("Here you have the list of the round names")
    print("and a number at the side of each name: ")
        
    for i in range(1,8):
        print(f" Round {i} - {i}")
    
    round_nb =verify_choice(
        "Your round number is? ",
        [str(x) for x in range(1,8)]
        )
    dt.append(round_nb)
    return dt,3


def select_or_create():
    print("  ---      You have three choices      ---")
    print("  -- < Add/check the players   - 0 > --")
    print("  -- < Select a tournament     - 1 > --")
    print("  -- < Create a new tournament - 2 > --")    
    content = "Please write '0', '1' or '2' "
    return verify_choice(content,['0','1','2'])


def select_tournament(tours):
    nb_tours = [str(x) for x in range(1,len(tours)+1)]
    content = f"For choosing the tournament write one of the numbers {' '.join(nb_tours)} "
    nb_tour = verify_choice(content,nb_tours)
    return tours[int(nb_tour)-1]

def choosed_tournament(tournament):
    print(f"You selected {tournament.name} at {tournament.place}")
    print(f"From {tournament.starting_date} to {tournament.ending_date}")
        
    if tournament.players_list == []:
        print("There are no players registred on this tournaments")
    else:
        print("The players registred at this turnament are: ")
        for pl_id in tournament.players_list:
            player = Player.from_db(pl_id)
            print(f"{player.first_name} {player.last_name}")


def select_round(round_nb):
    content = "You can choose the number of the round "
    return verify_choice(content,[str(x) for x in range(1,round_nb+1)])


def send_dt_round(round_nb):
    rnd = verify_choice(f"Write {round_nb} if it's the first round: ",[str(round_nb)])
    return rnd


# selecting players to add to the Tournament
def select_player4_tour(dt):
    list_players = []
    print(" You will have the first and the last name of each player\
write 'y' if you want to add this player to the tournament")
    content = "Write 'y' our yes and 'n' for no "
    for player in dt:
        print(f"Do you want to add {player.get('first_name')} {player.get('last_name')}")
        check = verify_choice(content,['y','n'])
        if check == 'y':
            list_players.append(player.get('id'))
    
    return list_players


#-----------------

def check_progress(welcome):
    check = None
    print(welcome)
    print("You can write 'yes' if you want to continue")
    print("or 'back' if you want to go back")
    check = input("Please write 'yes' or 'back' ")
    check.lower()

    while check not in ['yes', 'back']:
        print(" You might writed 'yes' or 'back' wrong ")
        check = input("Please write 'yes' or 'back' ")

    return check



def enter_player_data():
    welcome = "Welcome to the creation player part"
    check0 = check_progress(welcome)
  
    if check0 == 'back':
        return 'back'

    if check0 == 'yes':
        data = []
        firstname = input("Enter the players first name: ")
        data.append(firstname)
        lastname = input("Enter the players last name: ")
        data.append(lastname)
        print("for the player's birth date please follow this\
        format exemple: dd-mm-yyyy ")
        birthdate = input("Enter the player's birth date: ")
        data.append(birthdate)
        return data
