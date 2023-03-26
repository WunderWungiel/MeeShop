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

def options(db, addr):
    while True:
        while True:
            clean()
            print("  -------------------------------------- ")
            print(" |                                      |")
            print(" |         Welcome to {}MeeShop{}!          |".format(cyan, reset))
            print(" |                                      |")
            cat = "{}".format(addr)
            if len(cat) % 2 != 0:
                cat = cat + " "
            lenght = " " * int((38 - len(cat)) / 2) 
            print(" |{}{}{}{}{}{}|".format(lenght, blink, cyan, cat, reset, lenght))
            print(" |                                      |")
            print(" |          Select an option:           |")
            print(" |                                      |")
            print(" |             1. Search                |")
            print(" |             2. Show apps             |")
            print(" |             3. Return                |")
            print(" |                                      |")
            print(" |             0. Exit                  |")
            print(" |                                      |")
            print("  -------------------------------------- \n")
            option = input(" ")
            if not option:
                clean()
                continue
            print()
            if option not in ["1", "2", "3", "0"]:
                print(" {}Wrong number, select a correct one!{}".format(red, reset))
                print(" ")
                continue
            else:
                break

        if option == "1":
            clean()
            print("  -------------------------------------- ")
            print(" |                                      |")
            print(" |        Enter query, 0 to return:     |")
            print(" |                                      |")
            print("  -------------------------------------- \n")
            query = input(" {}Query to search:{} ".format(yellow, reset))
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
            print("  -------------------------------------- ")
            print(" |                                      |")
            print(" |           List of packages:          |")
            print(" |                                      |")
            for pkg in db.keys():

                if len(pkg) % 2 != 0:
                    pkg = pkg + " "
                lenght = " " * int((38 - len(pkg)) / 2)
                print(" |{}{}{}|".format(lenght, pkg, lenght))
            
            print(" |                                      |")
            print("  -------------------------------------- \n")
            input(" {}{}Press any key to continue... {}".format(blink, cyan, reset))
            clean()
            continue

        elif option == "3":
            return "Break"
        elif option == "0":
            clean()
            sys.exit(0) 