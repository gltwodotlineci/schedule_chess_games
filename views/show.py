from models.player import Player


def view_round_contest(data):
    print(" ")
    print("             The games are")
    for i,pl in enumerate(data):
        p1 = f"{pl[0].first_name} {pl[0].last_name}"
        p2 = f"{pl[1].first_name} {pl[1].last_name}"
        print("______        <>  <>  <>       ______")
        print(f"                 Game {i+1}")
        print(f"{p1} as white king vs {p2} as black king")
    print(" ")


def choosed_tournament(tournament):
    print(" ")
    print(f"You selected {tournament.name} at {tournament.place}")
    print(f"From {tournament.starting_date} to {tournament.ending_date}")
    if tournament.players_list == []:
        print("There are no players registred on this tournaments")
    else:
        print("The players registred of the turnament are: ")
        for pl_id in tournament.players_list:
            player = Player.from_db('id',pl_id)
            print(f"{player.first_name} {player.last_name} ")

    if tournament.rounds_list != []:
        print("The rounds for this turnament are.")
        for i in range(1,len(tournament.rounds_list)+1):
            print(f"Round {i}")


def add_winner_instruct():
    print('__________________________________________')
    print("               Entering the results     ")
    print(" ")
    print("To enter the results you will be asked to choose between the three posible cases")
    print("Write '1' if the player 1 won, '2' if the player 2 won, and '3' if it's a draw.")
    print("   ")


def after_contest(players):
    print(" ")
    print("The players points after the game are")
    for player in players:
        print(f"{player.first_name} {player.last_name} - {player.points} points")
