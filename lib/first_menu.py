import time

from .tui import TUIMenu, Item
from . import tui
from .wunder import menu as wunder_menu
from .openrepos import menu as openrepos_menu
from . import apt
from .rss import rss
from .small_libs import about, re_decoder, yellow, reset, red, blink, cyan, green, bold, press_enter, clean
from .stores.ovi import ovi_search

class OptionsActions:
    def __init__(self):
        pass

    def ovi(self):
        while True:
            while True:
                clean()
                tui.frame(text="Search:", second_frame=True)
                query = input(f"{yellow} Query to search:{reset} ")
                if not query:
                    clean()
                    continue
                if query == "0":
                    clean()
                    return "break"
                else:
                    break
            query = re_decoder(query)
            menu = ovi_search(query=query)
            menu.commit()
            while True:
                result = menu.show()
                if result == "break":
                    break
                
    def apt_fixer(self):
        apt.fix()
        clean()

    def update_repository(self):
        time.sleep(1)
        tui.rprint(" Updating repositories...")
        
        result = apt.update()

        if result == "Error":
            print(f" {red}Error updating repositories...{reset}")
            print(" Try to do it manually.")
        else:
            print(f" {green}Done!\n{reset}")

        input(f"{blink}{cyan} Press Enter to return... {reset}")
        clean()

    def check_for_updates(self):
        status = apt.meeshop_update()
        if status == "Error":
            print(f"{red} Error while checking updates...{reset}")
            press_enter()
        clean()

    def about(self):
        clean()
        about()
        clean()

    def donate(self):

        tui.frame(
            text = f"""{cyan}{bold}Donating{reset}
            
If you want to donate for my
work, you can do it here:

donationalerts.com/r/WunderWungiel

Thank you for every 
$, €, £, zł ♥

This really motivates.""",
            second_frame=False
        )

        press_enter()
        clean()

options_actions = OptionsActions()

menu = TUIMenu()

menu.text = '''Welcome to MeeShop
v0.3.0!'''

menu.items = [
    Item('OpenRepos', openrepos_menu, menu=True),
    Item('WunderW', wunder_menu, menu=True),
    Item('Ovi Store', options_actions.ovi),
    '',
    Item('RSS Feeds', rss, menu=True),
    Item('APT Fixer', options_actions.apt_fixer),
    Item('Update repository', options_actions.update_repository),
    Item('Check for updates', options_actions.check_for_updates),
    Item('Donate', options_actions.donate),
    Item('About', options_actions.about),
    '',
    Item('Exit', quit)
]

menu.commit()
