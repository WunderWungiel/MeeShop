import sys
from .clean import clean
from .search import search

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def init(lang):
    global strings
    if lang == "en":
        from langs.en import Strings
    elif lang == "ru":
        from langs.ru import Strings

    strings = Strings()

def options(db, addr, name):

    while True:
        while True:
            clean()
            strings.options_selection_list(name)
            option = input(" ")
            if not option:
                clean()
                continue
            print()
            if option not in ["1", "2", "3", "0"]:
                strings.wrong_number()
                print(" ")
                continue
            else:
                break

        if option == "1":
            clean()
            strings.enter_query_0()
            query = strings.query_to_search()
            if not query:
                clean()
                continue
            if query == "0":
                clean()
                continue
            else:
                search(db=db, query=query, addr=addr)
                clean()

        elif option == "2":
            clean()
            strings.show_apps_list()
            for pkg in db.keys():

                if len(pkg) % 2 != 0:
                    pkg = pkg + " "
                lenght = " " * int((38 - len(pkg)) / 2)
                print(" |{}{}{}|".format(lenght, pkg, lenght))
            
            print(" |                                      |")
            print("  -------------------------------------- \n")
            strings.press_enter_to_continue()
            clean()
            continue

        elif option == "3":
            return "Break"
        elif option == "0":
            clean()
            sys.exit(0) 