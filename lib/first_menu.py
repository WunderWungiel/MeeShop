from . import tui
from .wunder import menu as wunder_menu
from .openrepos import menu as openrepos_menu
from . import apt
from .rss import rss
from .small_libs import about, re_decoder, yellow, reset, red, blink, cyan, green, bold, press_enter
from .stores.ovi import ovi_search

class OptionsActions:
    def __init__(self):
        pass

    def openrepos(self):
        while True:
            _ = openrepos_menu()
            if _ == "Break":
                tui.clean()
                break

    def wunder(self):
        while True:
            _ = wunder_menu()
            if _ == "Break":
                tui.clean()
                break

    def ovi(self):
        while True:
            while True:
                tui.clean()
                tui.frame(text="Search:", second_frame=True)
                query = input(f"{yellow} Query to search:{reset} ")
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
            print(f" {red}Error updating repositories...{reset}")
            print(" Try to do it manually.")
        else:
            print(f" {green}Done!\n{reset}")

        input(f"{blink}{cyan} Press Enter to return... {reset}")
        tui.clean()

    def check_for_updates(self):
        status = apt.meeshop_update()
        if status == "Error":
            print(f"{red} Error while checking updates...{reset}")
            press_enter()
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

        press_enter()
        tui.clean()

options_actions = OptionsActions()

def first_menu():

    menu = tui.Menu()

    menu.text = '''Welcome to MeeShop
v0.3.0!'''

    menu.items = [
        ['OpenRepos', options_actions.openrepos],
        ['WunderW', options_actions.wunder],
        ['Ovi Store', options_actions.ovi],
        '',
        ['RSS Feeds', options_actions.rss_feeds],
        ['APT Fixer', options_actions.apt_fixer],
        ['Update repository', options_actions.update_repository],
        ['Check for updates', options_actions.check_for_updates],
        ['Donate', options_actions.donate],
        ['About', options_actions.about],
        '',
        ['Exit', quit]
    ]

    while True:
        tui.clean()
        result = menu.run()
        if result:
            return result
