from views.main_view import main_page

# main_page()

# while True:
#     main_page()




# ------

from controller.validator import ValidatePlayer, ValidateRound, ValidateTournament
player = None
player = ValidateTournament("AB12345","here","11-11-1111","13-11-1141","No desc","4")
print(player.__dict__)

#-----
