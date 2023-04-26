import sys

from .clean import clean
from .options import options
from .apt import Apt
from .rss import rss
from .about import about
from .re_decoder import re_decoder

from .search import Search
blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def init(database):
    global db
    global apt
    global search
    db = database
    apt = Apt()
    search = Search()

def category():

    while True:
        clean()
        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        print(" │       ╔═══════════════════════╗      │")
        print(" │       ║  Welcome to {}MeeShop{}!  ║      │".format(cyan, reset))
        print(" │       ╚═══════════════════════╝      │")
        print(" │                                      │")
        print(" │       {}Select category / option{}       │".format(blink, reset))
        print(" │                                      │")
        print(" │         1. Applications              │")
        print(" │         2. Ovi Store                 │")
        print(" │                                      │")
        print(" │         3. RSS Feeds                 │")
        print(" │         4. APT fixer                 │")
        print(" │                                      │")
        print(" │         5. Check for updates         │")
        print(" │         6. About                     │")
        print(" │                                      │")
        print(" │         0. Exit                      │")
        print(" │                                      │")
        print(" └──────────────────────────────────────┘ \n")
        supported = range(0, 7)
        category = input(" ")
        print()
        if not category:
            clean()
            continue
        if not category.isnumeric() or int(category) not in supported:
            continue
        else:
            break
    
    if category == "1":
        
        while True:
            _ = options(db)
            if _ == "Break":
                clean()
                break

    elif category == "2":

        while True:
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
                    clean()
                    return "Break"
                else:
                    break
            query = re_decoder(query)
            search.ovi_search(query=query)
            clean()

    elif category == "3":
        rss()
        clean()
        return
    elif category == "4":
        apt.fix()
        clean()
        return
    
    elif category == "5":
        apt.meeshop_update(db=db)
        clean()
        return

    elif category == "6":
        about()
        clean()
        return
    else:
        clean()
        sys.exit(0)