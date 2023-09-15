from . import tui
from . import app_functions
from .re_decoder import re_decoder
from . import dbc

db_creator = dbc.Db_creator()
ovi_db = db_creator.ovi_db
categories = db_creator.categories

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'


class Categories_Actions:
    def __init__(self):
        pass
    def category(self, category):
        while True:
            _ = app_functions.show_apps(category)
            if _ == "Break":
                return
    def exit(self):
        return "Break"

categories_actions = Categories_Actions()

class Options_Actions:
    def __init__(self):
        pass
    def search(self):
        while True:
            tui.clean()
            tui.frame(text="Search:")
            query = input("{} Query to search:{} ".format(yellow, reset))
            if not query:
                tui.clean()
                continue
            if query == "0":
                return "Break"
            else:
                query = re_decoder(query)
                app_functions.search(query=query, category="full")
                tui.clean()
    def categories(self):
        while True:
            tui.clean()

            options = {}
            args = {}

            dbs = {}

            for i, category in enumerate(categories.keys(), start=1):
                dbs[str(i)] = category

                name = categories[category]["name"]

                options[name] = categories_actions.category
                args[name] = dbs[str(i)]
            
            options["Return"] = categories_actions.exit

            while True:
                result = tui.menu(text="Categories:", options=options, args=args)
                if result:
                    return result

    def exit(self):
        return "Exit"

options_actions = Options_Actions()

def second_menu():

    text = "Welcome to MeeShop!"

    options = {
        'Search': options_actions.search,
        'Categories': options_actions.categories,
        'Return': options_actions.exit
    }

    while True:
        tui.clean()
        result = tui.menu(options=options, text=text)
        if result == "Exit":
            return "Break"