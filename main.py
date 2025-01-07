from views.main_view import main_page


def start_programme():
    status = True
    while status is True:
        status = main_page()


start_programme()
