from . import tui
from .stores.openrepos import search
from .small_libs import re_decoder
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
                search(query)
                tui.clean()
    def exit(self):
        return "Exit"

options_actions = OptionsActions()

def menu():

    menu = tui.Menu()

    menu.text = "OpenRepos.net"

    menu.items = [
        ['Search', options_actions.search], 
        '',
        ['Return', options_actions.exit]
    ]

    while True:
        tui.clean()
        result = menu.run()
        if result == "Exit":
            return "Break"
