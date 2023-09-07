import sys
from .tui import clean, menu
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

class Options_Actions:
    def __init__(self):
        pass
    def search(self):
        while True:
            clean()
            print(" ┌──────────────────────────────────────┐")
            print(" │                                      │")
            print(" │             ╔══════════╗             │")
            print(" │             ║  Search: ║             │")
            print(" │             ╚══════════╝             │")
            print(" │                                      │")
            print(" └──────────────────────────────────────┘ \n")
            query = input(" {}Query to search:{} ".format(yellow, reset))
            if not query:
                clean()
                continue
            if query == "0":
                return "Break"
            else:
                query = re_decoder(query)
                app_functions.search(query=query, category="full")
                clean()
    def categories(self):
        while True:
            clean()
            print(" ┌──────────────────────────────────────┐")
            print(" │                                      │")
            print(" │           ╔══════════════╗           │")
            print(" │           ║  Categories: ║           │")
            print(" │           ╚══════════════╝           │")
            print(" │                                      │")

            dbs = {}

            for i, category in enumerate(categories.keys(), start=1):
                dbs[str(i)] = category

                name = categories[category]["name"]

                text = "           {}. {}".format(str(i), name)
                lenght = " " * int((38 - len(text)))
                text = text = "           {}. {}{}".format(str(i), name, lenght)
                print(" │{}│".format(text))


            print(" │                                      │")
            print(" │           0. Return                  │")
            print(" │                                      │")
            print(" └──────────────────────────────────────┘ \n")

            while True:
                answer = input(" {}Select category or return:{} ".format(cyan, reset))

                if answer == "0":
                    return "Break"
                if not answer.isnumeric() or answer not in dbs.keys():
                    continue

                _ = app_functions.show_apps(dbs[answer])
                if _ == "Break":
                    return "Break"

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
        clean()
        result = menu(text, options)
        if result == "Exit":
            return "Break"