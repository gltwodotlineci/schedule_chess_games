from views.main_view import main_page

# main_page()

# while True:
#     main_page()




# ------
from models.round import Round
from controller.validator import ValidateRound
data = {
    'tournament_id':'',
    'name':'',
    'number':'',
    'starting_date_hour':'11-11-1111-11-11',
    
        }
rd = Round(1,2,3,4)



# players = [
#     "327PermetiAndon","325ZeqoPilafi" ,"794KasemTrepeshina",
#     "262AqifKapertoni","723BicakuKasnec","717AfrimTahipi",
#     "498Mazlleku","504NanastasJanusqetlla"
# ]



# game_list1 = [
#     ['327PermetiAndon', '794KasemTrepeshina'],
#     ['723BicakuKasnec', '717AfrimTahipi'],
#     ['325ZeqoPilafi', '504NanastasJanusqetlla'],
#     ['498Mazlleku', '262AqifKapertoni']
# ]

# game_list2 = []

# used_combinations = set(tuple(sorted(combination)) for combination in game_list1)

# for i in range(0, len(players), 2):
#     if i + 1 < len(players):
#         player1, player2 = sorted([players[i], players[i+1]])
#         combination_key = tuple(player1), tuple(player2)
#         if combination_key not in used_combinations:
#             game_list2.append([player1, player2])

# print("game_list2:", game_list2)





#-----
