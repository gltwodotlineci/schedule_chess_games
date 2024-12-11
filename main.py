# from controller.controller import create_player
# from controller.controller import create_round
# from controller.controller import planing_games
# from controller.controller import create_tournament
# from controller.controller import add_round_2tournement
# from controller.controller import add_after_game

from views.main_view import welcome_page
from views.main_view import mock_creating
from views.lists_values import show_all_players
from views.main_view import mock_show

# from controller.controller import list_tournaments_players
while True:
    mock_show()



mock_show()


#create_round()
def creating_tour_round_or_player():
    given_dt = mock_creating()
    if given_dt[1] == 1:
        pass
        # create_tournament(given_dt[0])
    elif given_dt[1] == 2:
        pass
        # return create_player(given_dt[0])
    elif given_dt[1] == 3:
        pass
        # create_round(given_dt[0])




