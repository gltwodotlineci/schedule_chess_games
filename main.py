from views.main_view import main_page

# main_page()

# while True:
#     main_page()




# ------

from controller.validator import ValidatePlayer, ValidateRound, ValidateTournament
from controller.controller import create_round, create_tournament, create_player


data = {
    'fin':"ZZ1234k",
    'first_name':"testname",
    'last_name': "testlastname",
    'birth_date': '11-11-1111'
}

player = create_player(data)
print(player.__dict__)
#-----
