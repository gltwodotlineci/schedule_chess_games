from views.choose_dt import verify_choice
from views.choose_dt import send_dt_tourn
from views.choose_dt import send_dt_player
from views.choose_dt import select_or_create
from views.choose_dt import select_tournament
from views.choose_dt import ask_add_player
from views.choose_dt import create_round_tour
from views.choose_dt import confirm_creation
from views.choose_dt import date_and_time
from views.choose_dt import choos_winner
from views.choose_dt import choos_fed_nb
from views.choose_dt import go_back
from views.show import after_contest

from views.show import view_round_contest
from views.show import add_winner_instruct
from views.show import choosed_tournament

from views.lists_values import show_all_tournaments
from views.lists_values import show_all_players

from views.rapport import create_html_rapport


from controller.controller import all_tournaments
from controller.controller import list_tournaments_players
from controller.controller import create_tournament
from controller.controller import create_round
from controller.controller import create_player
from controller.controller import create_round
from controller.controller import order_players
from controller.controller import organize_game
from controller.controller import add_player2_tour
from controller.controller import games_by_round
from controller.controller import round_players
from controller.controller import add_results
from controller.controller import calculate_points
from controller.controller import sort_players_rnd2
from controller.controller import get_current_round
from controller.controller import selected_games
from controller.controller import create_rapport
from controller.controller import tournament_players
from controller.controller import edit_tour_round




def welcom_header(data):
    print("--- WELCOME TO THE CHESS GAME APPLICATION! ---")
    print(f"You have registred {len(data['tournaments'])} tournements")
    print(f"You alsow have {len(data['players'])} players")
    print('                ')


def palyer_menu_1():
    print(" ")
    print("     Your Players Are:")
    show_all_players()
    return ask_add_player()


def add_player(player):
    create_player(player)
    print("Write 'stop' if you don't want to add more players")
    print("Or write 'continue' if you want to add an other player")
    content = "Write 'stop' or 'continue' " 
    stp_cnt = verify_choice(content,['stop','continue'])
    if stp_cnt == 'stop':
        return False

    return True


def choose_tour():
    print(" ")
    show_all_tournaments()
    tour = select_tournament(all_tournaments())
    choosed_tournament(tour)
    return tour


def finish_or_cont(para_rd1, para_rd2):
    # if actual_round == tour.round_numbers:
    if para_rd1 == para_rd2:
        print("All the rounds of this tournament have been played")
        content = "Write 'back' to go to the main page "
        back = verify_choice(content,['back'])
        if back == 'back':
            return 'back'

    print("You can now start organzing the games or go back")
    content = "write 'yes' or 'back' "
    start_games = verify_choice(content,['yes','back'])
    if start_games == 'back':
        return 'back'



def main_page():
    welcom_header(list_tournaments_players())
    print(" -*-*-*-  -*-*-*- -*-*-*- -*-*-*-")
    choice0 = select_or_create()
    if choice0 == '1':
        if palyer_menu_1() == 'yes':
            new_player = True
            while new_player is True:
                player = send_dt_player()
                new_player = add_player(player)
        else:
            return True
        # go back to main menue
        if go_back() == 'back':
            return True
        return False

    if choice0 == '2':
        tour = choose_tour()
        #Organizing games by round.
        actual_round = tour.actual_round_number
        cont_back = finish_or_cont(actual_round, tour.round_numbers)
        if cont_back == 'back':
            return True

        # get the courrent round
        while actual_round < tour.round_numbers:
            print("--------")
            print("Round ", actual_round+1)
            print("--------")
            round = get_current_round(tour)
            if tour.actual_round_number < 1:    
                sorted_players = order_players(tour.players_list,True)
            else:
                games = selected_games('round_id',str(round.id))
                actual_players = calculate_points(tour)
                new_sorted_players_id = sort_players_rnd2(actual_players,games)
                sorted_players = order_players(new_sorted_players_id)

            games = organize_game(sorted_players, round)
            # adding list games to the round
            lst_games_id = [str(x.id) for x in games]
            round.games_list = lst_games_id
            round.save(str(round.id))
            # Geting round and creating games for round        
            round_games = games_by_round(str(round.id))
            players, games = round_players(round_games)
            view_round_contest(players,games)
            add_winner_instruct()
            games = choos_winner(players,games)
            tour = edit_tour_round(round)
            # check the players points based on games results
            actual_players = calculate_points(tour)
            after_contest(actual_players)
            # Checking if all rounds have been played
            actual_round = tour.actual_round_number
            if actual_round == tour.round_numbers:
                break

            print("If you want to continue or go back write 'c' or 'back'")
            content = "write 'c' or 'back' "
            cont_back = verify_choice(content,['c','back'])
            if cont_back == 'back':
                break
            return True

    elif choice0 == '3':
        print(" ")
        print("Lets create some Tournaments ! ")
        dt_tournament = send_dt_tourn()
        tour = create_tournament(dt_tournament)
        print(" ")
        print("From the next player list you can choose the players for this tournament")
        print("The number of players must be even. ")
        print(" ")
        show_all_players()
        print("_________________")

        nb_players = int(tour.nb_players)
        print("Exemple of the FED Id nb 'AB12345' ")
        for i in range(1,nb_players+1):
            add_player2_tour(tour,choos_fed_nb(tour,i))
        
        print(" ")
        
        choice1 = create_round_tour(tour)
        if choice1 == 'back':
            return True

        # creating all the rounds
        existing_round = len(tour.rounds_list)
        needed_rounds = tour.round_numbers
        rounds = []
        for i in range(existing_round,needed_rounds):
            data = date_and_time(i)
            data['tournament_id'] = str(tour.id)
            rounds.append(create_round(data))

        print(f"Congratulation, You have created the {tour.name} tournament")
        retour = verify_choice("write 'yes' to go to the main menue or 'C' to close: ",['yes', 'close'])
        if retour == 'yes':
            return True
        return False

    elif choice0 == 'R':
        print(" Creating rapport based on choosed tournament: ")
        print(" ")
        # The tournaments
        show_all_tournaments()
        choosed_tour = select_tournament(all_tournaments())
        # creating rapports
        rapport = create_rapport()
        rapport.choosed_tour = choosed_tour.id
        tour_choice = rapport.choosed_tour
        print("  ")
        print(f"The selected tournament is: {tour_choice.get('name')} starting at {tour_choice.get('starting_date')} ending at {tour_choice.get('ending_date')}")
        # create html rapport
        create_html_rapport(rapport)
        return True
    else:
        return False


#---------------- Test part


#------------------