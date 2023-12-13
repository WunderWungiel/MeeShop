from . import tui
from .stores.openrepos import or_search, or_categories
from .small_libs import re_decoder, quit
from .dbc import categories

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

class OptionsActions:
    def __init__(self):
        pass
    
    def search(self):
        while True:
            tui.clean()
            tui.frame(text="Search:", second_frame=True)
            query = input(f"{yellow} Query to search:{reset} ")
            if not query:
                tui.clean()
                continue
            if query == "0":
                return "Break"
            else:
                query = re_decoder(query)
                or_search(query)
                tui.clean()

    def categories(self):
        while True:
            result = or_categories()
            print(result)
            if result:
                return result

    def exit(self):
        return "Exit"

options_actions = OptionsActions()

def menu():

    menu = tui.TUIMenu()

    menu.text = "OpenRepos.net"

    menu.items = [
        ['Search', options_actions.search], 
        ['Categories', options_actions.categories],
        '',
        ['Return', options_actions.exit]
    ]

    menu.commit()

    while True:
        tui.clean()
        result = menu.show()
        if result == "Exit":
            return "Break"
