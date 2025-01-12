import sys
sys.path.append("/opt/MeeShop/lib")
from clean import clean
from second_menu import second_menu
import apt
from rss import rss
from about import about
from re_decoder import re_decoder
import app_functions

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def first_menu():

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
        print(" │         5. Update repository         │")
        print(" │                                      │")
        print(" │         6. Check for updates         │")
        print(" │         7. About                     │")
        print(" │                                      │")
        print(" │         0. Exit                      │")
        print(" │                                      │")
        print(" └──────────────────────────────────────┘ \n")
        supported = range(0, 8)
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
            _ = second_menu()
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
            app_functions.ovi_search(query=query)
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

        print(" Updating repositories...\n")
        
        result = apt.update()

        if result == "Error":
            print(" {}Error updating repositories...{}".format(red, reset))
            print(" Try to do it manually.")
        else:
            print(" {}Done!\n{}".format(green, reset))

        input(" {}{}Press Enter to return... {}".format(blink, cyan, reset))
        clean()
        return

    elif category == "6":
        apt.meeshop_update()
        clean()
        return

    elif category == "7":
        about()
        clean()
        return
    else:
        clean()
        sys.exit(0)