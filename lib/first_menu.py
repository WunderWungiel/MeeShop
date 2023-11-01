from . import tui
from .second_menu import second_menu
from . import apt
from .rss import rss
from .small_libs import about, re_decoder, yellow, reset, red, blink, cyan, green, bold
from .stores.ovi import ovi_search
from .stores import openrepos

class OptionsActions:
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
                tui.frame(text="Search:", second_frame=True)
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
            ovi_search(query=query)
            tui.clean()

    def openrepos(self):
        while True:
            while True:
                tui.clean()
                tui.frame(text="Search:", second_frame=True)
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
            openrepos.search(query=query)
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
        tui.clean()
        about()
        tui.clean()

    def donate(self):

        tui.frame(
            text = f"""{cyan}{bold}Donating{reset}
            
If you want to donate for my
small work, you can do it here:

donationalerts.com/r/WunderWungiel

Thank you for every 
$, €, £, zł, etc., etc. ♥

This really motivates.""",
            second_frame=False
        )

        tui.press_enter()
        tui.clean()

options_actions = OptionsActions()

def first_menu():

    text = '''Welcome to MeeShop
v0.3.0!'''

    items = [
        ['Search in OR', options_actions.openrepos],
        ['Applications', options_actions.second_menu],
        ['Ovi Store', options_actions.ovi_store],
        ['RSS Feeds', options_actions.rss_feeds],
        ['APT Fixer', options_actions.apt_fixer],
        ['Update repository', options_actions.update_repository],
        ['Check for updates', options_actions.check_for_updates],
        ['Donate', options_actions.donate],
        ['About', options_actions.about],
        ['Exit', quit]
    ]

    while True:
        tui.clean()
        result = tui.menu(items, text=text)
        if result:
            return result
