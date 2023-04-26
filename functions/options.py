from .clean import clean
from .search import Search
from .re_decoder import re_decoder

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def init():
    global search
    search = Search()

def options(db):

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
            print(" │             2. Show apps             │")
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
                search.search(db=db, query=query)
                clean()

        elif option == "2":
            clean()
            print(" ┌──────────────────────────────────────┐")
            print(" │                                      │")
            print(" │         ╔════════════════════╗       │")
            print(" │         ║  List of packages: ║       │")
            print(" │         ╚════════════════════╝       │")
            print(" │                                      │")
            for pkg in db.keys():
                pkg = db[pkg]['display_name']
                if len(pkg) % 2 != 0:
                    pkg = pkg + " "
                lenght = " " * int((38 - len(pkg)) / 2)
                print(" │{}{}{}│".format(lenght, pkg, lenght))
            
            print(" │                                      │")
            print(" └──────────────────────────────────────┘ \n")
            input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
            clean()
            continue

        elif option == "0":
            return "Break"