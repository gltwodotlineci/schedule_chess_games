from models.player import Player
from models.round import Round
from models.tournament import Tournament

# validating the datas for the player creation
class ValidatePlayer(Player):
    def __init__(self, fin, first_name, last_name, birth_date):
        self._birth_date = birth_date
        super().__init__(fin, first_name, last_name, birth_date)

    @property
    def birth_date(self):
        return self._birth_date


    @property
    def fin(self):
        return self._fin


    @birth_date.setter
    def birth_date(self, val):
        if val[2] != '-' or val[5] != '-' or len(val) != 10:
            raise ValueError("Wrong date format, please retry with this format 'dd-mm-yyyy' ")
        else:
            self._birth_date = val


    @fin.setter
    def fin(self,nb):
        if nb[0:2].isdigit() or nb[2:].isdigit() == False or len(nb) != 7:
            raise ValueError("Wrong 'fin' format, please retray with the format 'AB12345' " )
        else:
            self._fin = nb



# validating the datas for the round creation
class ValidateRound(Round):
    def __init__(self, tournament_id, name, number):
        self._number = number
        super().__init__(tournament_id, name, number)

    @property
    def number(self):
        return self._number


    @number.setter
    def number(self, nb_val):
        if nb_val.is_integer():
            self._number = nb_val
        else:
            raise ValueError("Wrong number choise, Please be sure to choose a number ")


# validating the datas for the tournament creation
class ValidateTournament(Tournament):
    def __init__(self, name, place, starting_date, ending_date, description, nb_players, rounds_list=[], players_list=[], round_numbers=4, actual_round_number=0):
        super().__init__(name, place, starting_date, ending_date, description, nb_players, rounds_list, players_list, round_numbers, actual_round_number)
        self._starting_date = starting_date
        self._ending_date = ending_date

    @property
    def starting_date(self):
        return self._starting_date


    @property
    def ending_date(self):
        return self._ending_date
    

    @property
    def nb_players(self):
        return self._nb_players


    @starting_date.setter
    def starting_date(self, val):
        if val[2] != '-' or val[5] != '-' or len(val) != 10:
            raise ValueError("Wrong date format, please retry with this format 'dd-mm-yyyy' ")
        else:
            self._starting_date = val
        

    @starting_date.setter
    def ending_date(self, val):
        if val[2] != '-' or val[5] != '-' or len(val) != 10:
            raise ValueError("Wrong date format, please retry with this format 'dd-mm-yyyy' ")
        else:
            self._ending_date = val


    @nb_players.setter
    def nb_players(self,nb):
        if int(nb) % 2 != 0 or nb.isnumeric() == False:
            raise ValueError("Error, the number of players must be an even number ")
        else:
            self._nb_players = nb


class ValidateRound(Round):
    def __init__(self, tournament_id, name, number, starting_date_hour, ending_date_hour=None):
        super().__init__(tournament_id, name, number, starting_date_hour, ending_date_hour)

        self._starting_date_hour = starting_date_hour

    @property
    def starting_date_hour(self):
        return self._starting_date_hour


    @starting_date_hour.setter
    def starting_date_hour(self,date):
        if len(date) != 16:
            raise ValueError("Please verify your starting date format")
        elif '-' not in [date[2],date[5],date[10],date[13]]:
            raise ValueError("Write your starting date-hour at this format 'dd-mm-yyyy-hh-mm'")
        else:
            self._starting_date_hour = date
