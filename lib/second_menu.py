from . import tui
from .stores.wunder import show_apps, search
from .small_libs import re_decoder
from .dbc import categories

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'


class CategoriesActions:
    def __init__(self):
        pass
    def category(self, category):
        while True:
            _ = show_apps(category)
            if _ == "Break":
                return
    def exit(self):
        return "Break"

categories_actions = CategoriesActions()

class OptionsActions:
    def __init__(self):
        pass
    def search(self):
        while True:
            tui.clean()
            tui.frame(text="Search:")
            query = input("{} Query to search:{} ".format(yellow, reset))
            if not query:
                tui.clean()
                continue
            if query == "0":
                return "Break"
            else:
                query = re_decoder(query)
                search(query=query, category="full")
                tui.clean()
    def categories(self):
        while True:
            tui.clean()

            items = []

            dbs = {}

            for i, category in enumerate(categories.keys(), start=1):
                dbs[str(i)] = category

                name = categories[category]["name"]

                items.append([name, categories_actions.category, [dbs[str(i)]]])
            
            items.append(["Return", categories_actions.exit])

            while True:
                result = tui.menu(items=items, text="Categories:")
                if result:
                    return result

    def exit(self):
        return "Exit"

options_actions = OptionsActions()

def second_menu():

    text = "Welcome to MeeShop!"

    items = [
        ['Search', options_actions.search],
        ['Categories', options_actions.categories],
        ['Return', options_actions.exit]
    ]

    while True:
        tui.clean()
        result = tui.menu(items, text=text)
        if result == "Exit":
            return "Break"
