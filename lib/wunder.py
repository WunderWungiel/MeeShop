from . import tui
from .tui import Item, TUIMenu
from .stores.wunder import show_apps, search
from .small_libs import re_decoder, reset, yellow
from .dbc import categories

def search_popup():
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
            menu = search(query=query, category="full")
            while True:
                result = menu.show()
                if result == "break":
                    return

categories_menu = TUIMenu(text="Categories:")
dbs = {}
for i, category in enumerate(categories.keys(), start=1):
    dbs[str(i)] = category

    name = categories[category]["name"]
    categories_menu.items.append(Item(name, show_apps, category, menu=True))            

categories_menu.items += ['', Item("Return", returns=True)]

menu = TUIMenu()

menu.text = "Welcome to MeeShop!"

menu.items = [
    Item('Search', search_popup), 
    Item('Categories', categories_menu, menu=True),
    '',
    Item('Return', returns=True)
]
