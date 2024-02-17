from time import sleep

from .tui import TUIMenu, Item
from . import tui
from .stores.openrepos import or_search, categories_menu
from .small_libs import re_decoder

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

class OptionsActions:
    
    def search(self):
        while True:
            tui.clean()
            tui.frame(text="Search:", second_frame=True)
            query = input(f"{yellow} Query to search:{reset} ")
            if not query:
                tui.clean()
                continue
            if query == "0":
                return "break"
            else:
                query = re_decoder(query)
                if len(query) <= 3:
                    print(f" {red}Search query has to be 4-letters long or longer!{reset}")
                    sleep(1)
                    continue
                while True:
                    result = or_search(query)
                    if result:
                        return

options_actions = OptionsActions()

menu = TUIMenu(text = "OpenRepos.net")

menu.items = [
    Item('Search', options_actions.search), 
    Item('Categories', categories_menu),
    '',
    Item('Return', returns=True)
]