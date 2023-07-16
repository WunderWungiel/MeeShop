import sys
sys.path.append("/opt/MeeShop/functions")
from clean import clean
import app_functions
from re_decoder import re_decoder
import dbc

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

def second_menu():

    while True:
        while True:
            clean()
            print(" ┌──────────────────────────────────────┐")
            print(" │                                      │")
            print(" │       ╔═══════════════════════╗      │")
            print(" │       ║  Welcome to {}MeeShop{}!  ║      │".format(cyan, reset))
            print(" │       ╚═══════════════════════╝      │")
            print(" │                                      │")
            print(" │          Select an option:           │")
            print(" │                                      │")
            print(" │             1. Search                │")
            print(" │             2. Categories            │")
            print(" │                                      │")
            print(" │             0. Return                │")
            print(" │                                      │")
            print(" └──────────────────────────────────────┘ \n")
            option = input(" ")
            if not option:
                clean()
                continue
            print()
            if option not in ["1", "2", "0"]:
                print(" {}Wrong number, select a correct one!{}".format(red, reset))
                print(" ")
                continue
            else:
                break

        if option == "1":
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
                clean()
                continue
            else:
                query = re_decoder(query)
                app_functions.search(query=query, category="full")
                clean()

        elif option == "2":

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

 

                _break = None

                while True:
                    answer = input(" {}Select category or return:{} ".format(cyan, reset))

                    if answer == "0":
                        _break = True
                        break

                    if not answer.isnumeric() or answer not in dbs.keys():
                        continue

                    _ = app_functions.show_apps(dbs[answer])
                    if _ == "Break":
                        break

                if _break:
                    _break = None
                    break

        elif option == "0":
            return "Break"