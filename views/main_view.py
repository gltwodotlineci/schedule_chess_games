from views.choose_dt import verify_choice
from views.choose_dt import send_dt_tourn
from views.choose_dt import send_dt_player
from views.choose_dt import select_or_create
from views.choose_dt import select_tournament
from views.choose_dt import ask_add_player
from views.choose_dt import create_round_tour
from views.choose_dt import date_and_time
from views.choose_dt import choos_winner
from views.choose_dt import choos_fed_nb
from views.choose_dt import go_back
from views.choose_dt import nn_complet_tour
from views.show import after_contest

from views.show import view_round_contest
from views.show import add_winner_instruct
from views.show import choosed_tournament

from views.lists_values import show_all_tournaments
from views.lists_values import show_all_players

from views.report import create_html_report

from controller.controller import all_tournaments
from controller.controller import all_players
from controller.controller import create_tournament
from controller.controller import create_round
from controller.controller import create_player
from controller.controller import order_players
from controller.controller import organize_game
from controller.controller import add_player2_tour
from controller.controller import games_by_round
from controller.controller import round_players
from controller.controller import calculate_points
from controller.controller import sort_players_rnd2
from controller.controller import get_current_round
from controller.controller import selected_games
from controller.controller import create_report
from controller.controller import edit_tour_round
from controller.controller import check_last_tour
from controller.controller import new_game_players
from controller.controller import get_passed_round


def welcom_header(tours, players):
    print("--- WELCOME TO THE CHESS GAME APPLICATION! ---")
    print(f"You have registred {len(tours)} tournements")
    print(f"You alsow have {len(players)} players")
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
    stp_cnt = verify_choice(content, ['stop', 'continue'])
    if stp_cnt == 'stop':
        return False

    return True


def choose_tour():
    print(" ")
    show_all_tournaments()
    # checking if the tournament construction is complete
    tour = select_tournament(all_tournaments())
    completed, tour, missing_pl, missing_rd = check_last_tour(tour)
    if completed is False:
        return nn_complet_tour(tour, missing_pl, missing_rd)

    choosed_tournament(tour)
    return tour


'''
Part 2 menue
'''


def finish_or_cont(para_rd1, para_rd2):
    # if actual_round == tour.round_numbers:
    if para_rd1 == para_rd2:
        print("All the rounds of this tournament have been played")
        content = "Write 'back' to go to the main page "
        back = verify_choice(content, ['back'])
        if back == 'back':
            return 'back'

    print("You can now start organzing the games or go back")
    content = "write 'yes' or 'back' "
    start_games = verify_choice(content, ['yes', 'back'])
    if start_games == 'back':
        return 'back'


def sort_players(tour):
    actual_round = tour.actual_round_number
    print("--------")
    print("Round ", actual_round+1)
    print("--------")
    round = get_current_round(tour)

    if actual_round < 1:
        sorted_players = order_players(tour.players_list, True)
    else:
        passed_rd = get_passed_round(tour)
        games = selected_games('round_id', passed_rd.id)
        actual_players = calculate_points(tour)
        new_sorted_players_id = new_game_players(actual_players, games)
        new_sorted_players_id = sort_players_rnd2(actual_players, games)
        sorted_players = order_players(new_sorted_players_id)

    return round, sorted_players


def ending_menu2():
    print("You played all the rounds of this turnament!")
    print("If you want to close or go back write 'C' or 'back'")
    content = "'C' for close and 'back' for going back "
    cont_back = verify_choice(content, ['C', 'back'])
    if cont_back == 'back':
        return True
    return False


'''
Part 3 menue
'''


def players_for_new_tour():
    print(" ")
    complete, lst_tour, missing_pls, missing_rds = check_last_tour()
    if complete is False:
        if missing_rds > 0 and missing_pls == 0:
            msng = f"Your tournament {lst_tour.name} is missing"
            msng += f" {missing_rds} rounds"
            print(msng)
            restart = "You can restart creating the missed"
            restart += " rounds for this tournament"
            print(restart)
            return lst_tour, missing_pls
        print("You haven't added all the players to your last tournament")
        lst_tour = f"In your tournament '{lst_tour.name}' you need"
        lst_tour += f" to add {missing_pls} player/s"
        print(lst_tour)
        nb_players = len(lst_tour.players_list)
        show_all_players()
        return lst_tour, missing_pls

    print("Lets create some Tournaments ! ")
    dt_tournament = send_dt_tourn()
    tour = create_tournament(dt_tournament)
    print(" ")
    nxt_pl = "From the next player list you can choose"
    nxt_pl += " the players for this tournament"
    print(nxt_pl)
    print("The number of players must be even. ")
    print(" ")
    show_all_players()
    print("_________________")
    nb_players = int(tour.nb_players)
    print("Exemple of the FED Id nb 'AB12345' ")
    return tour, nb_players


'''
    MAIN MENUE
'''


def main_page():
    welcom_header(all_tournaments(), all_players())
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
        if tour == 'back':
            return True
        # Organizing games by round.
        actual_round = tour.actual_round_number
        cont_back = finish_or_cont(actual_round, tour.round_numbers)
        if cont_back == 'back':
            return True

        # get the courrent round
        while actual_round < tour.round_numbers:
            round, sorted_players = sort_players(tour)
            games = organize_game(sorted_players, round)
            # adding list games to the round
            lst_games_id = [str(x.id) for x in games]
            round.games_list = lst_games_id
            round.save(str(round.id))
            # Geting round and creating games for round
            round_games = games_by_round(str(round.id))
            players, games = round_players(round_games)
            view_round_contest(players, games)
            add_winner_instruct()
            games = choos_winner(players, games)
            tour = edit_tour_round(round)
            # check the players points based on games results
            actual_players = calculate_points(tour)
            after_contest(actual_players)
            # Checking if all rounds have been played
            actual_round = tour.actual_round_number
            if actual_round == tour.round_numbers:
                break

        return ending_menu2()

    elif choice0 == '3':
        tour, nb_players = players_for_new_tour()
        for i in range(1, nb_players+1):
            add_player2_tour(tour, choos_fed_nb(tour, i))

        print(" ")
        choice1 = create_round_tour(tour)
        if choice1 == 'back':
            return True

        # creating all the rounds
        existing_round = len(tour.rounds_list)
        needed_rounds = tour.round_numbers
        rounds = []
        for i in range(existing_round, needed_rounds):
            data = date_and_time(i)
            data['tournament_id'] = str(tour.id)
            rounds.append(create_round(data))
        print(f"Congratulation, You have created the {tour.name} tournament")
        content_b = "write 'yes' to go to the main menue or 'C' to close: "
        retour = verify_choice(content_b, ['yes', 'close'])
        if retour == 'yes':
            return True
        return False

    elif choice0 == 'R':
        print(" Creating report based on choosed tournament: ")
        print(" ")
        # The tournaments
        show_all_tournaments()
        choosed_tour = select_tournament(all_tournaments())
        # creating reports
        report = create_report()
        report.choosed_tour = choosed_tour.id
        tour_choice = report.choosed_tour
        print("  ")
        slct_tr = f"The selected tournament is: {tour_choice.get('name')}"
        slct_tr += f"starting at {tour_choice.get('starting_date')}"
        slct_tr += f" ending at {tour_choice.get('ending_date')}"
        print(slct_tr)
        # create html report
        create_html_report(report)
        return True
    else:
        return False
