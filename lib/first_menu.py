import sys
from . import tui
from .second_menu import second_menu
from . import apt
from .rss import rss
from .about import about
from .re_decoder import re_decoder
from . import app_functions

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
    def second_menu(self):
        while True:
            _ = second_menu()
            if _ == "Break":
                tui.clean()
                break
    def ovi_store(self):
        while True:
            while True:
                tui.clean()
                tui.frame(text="Search:")
                query = input("{} Query to search:{} ".format(yellow, reset))
                if not query:
                    tui.clean()
                    continue
                if query == "0":
                    tui.clean()
                    return "Break"
                else:
                    break
            query = re_decoder(query)
            app_functions.ovi_search(query=query)
            tui.clean()
    def rss_feeds(self):
        rss()
        tui.clean()
    def apt_fixer(self):
        apt.fix()
        tui.clean()
    def update_repository(self):
        tui.rprint(" Updating repositories...")
        
        result = apt.update()

        if result == "Error":
            print(" {}Error updating repositories...{}".format(red, reset))
            print(" Try to do it manually.")
        else:
            print(" {}Done!\n{}".format(green, reset))

        input("{}{} Press Enter to return... {}".format(blink, cyan, reset))
        tui.clean()
    def check_for_updates(self):
        status = apt.meeshop_update()
        if status == "Error":
            print(f"{red} Error while checking updates...{reset}")
            tui.press_enter()
        tui.clean()
    def about(self):
        about()
        tui.clean()
    def exit(self):
        sys.exit(0)

options_actions = Options_Actions()

def first_menu():

    text = "Welcome to MeeShop!"

    options = {
        'Applications': options_actions.second_menu,
        'Ovi Store': options_actions.ovi_store,
        'RSS Feeds': options_actions.rss_feeds,
        'APT Fixer': options_actions.apt_fixer,
        'Update repository': options_actions.update_repository,
        'Check for updates': options_actions.check_for_updates,
        'About': options_actions.about,
        'Exit': options_actions.exit
    }

    while True:
        tui.clean()
        result = tui.menu(options=options, text=text)
        if result:
            return result