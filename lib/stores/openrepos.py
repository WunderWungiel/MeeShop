import re

from .. import tui
from .. import api
from .. small_libs import red, reset, yellow, press_enter

class ORAppOptionsActions:
    def __init__(self):
        pass
    def files(self, files):

        print(files)

        class FilesOptionsActions:
            def __init__(self):
                pass
            def get_file(self, link):
                pass
            def exit(self):
                return "Break"

        files_options_actions = FilesOptionsActions()

        menu = tui.TUIMenu(text="Files", space_left=5)

        for file, link in files.items():
            menu.items.append([
                file, files_options_actions.get_file, link
            ])
        menu.items += ['', ["Return", files_options_actions.exit]]

        menu.commit()

        while True:
            _ = menu.show()
            if _ == "Break":
                break

    def description(self):
        pass

    def exit(self):
        return "Break"
        
or_app_options_actions = ORAppOptionsActions()

def or_app(link):
    tui.clean()

    app_info = api.get_app_info(link)
    title, stars = app_info.title, app_info.stars

    if len(title) % 2 != 0:
        title = title + " "

    custom_text = tui.frame_around_text(title)
    custom_text += f"""\n │                                      │"""
    
    stars_string = ''
    for star_status in stars.values():
        if star_status == "on":
            stars_string += "⭐"
        else:
            stars_string += " "
    lenght = " " * int((38 - 15 - len(stars_string)))

    custom_text += f"\n │  Rating: {stars_string}{lenght}│"

    maintainer = app_info.author

    lenght = " " * int((38 - 14 - len(maintainer)))
    custom_text += f"""
 │  Maintainer: {maintainer}{lenght}│
 │                                      │"""

    menu = tui.TUIMenu(custom_text=custom_text)

    menu.items = [
        ['Files', or_app_options_actions.files, app_info.files],
        ['Description', or_app_options_actions.description, app_info.description],
        '',
        ['Return', or_app_options_actions.exit]
    ]

    menu.commit()

    while True:
        result = menu.show()
        if result:
            return result

def category_link(name, link):
    ic(name, link)
    quit(0)
    pass

def return_break():
    return "Break"

def sub_cat_menu(main_cat, sub_categories):
    menu = tui.TUIMenu()
        
    menu.items.append((main_cat[0], category_link, (main_cat[0], main_cat[1])))

    for name in sub_categories.keys():

        menu.items.append(
            [
                name,
                category_link,
                [name, sub_categories[name]]
            ]
        )

    menu.items += ('', ["Return", return_break])

    menu.commit()

    while True:
        result = menu.show()
        if result:
            return result

def or_categories():

    categories = api.get_categories()

    menu = tui.TUIMenu()

    for name in categories.keys():

        print(name)

        if "categories" in categories[name]:
            
            menu.items.append(
                [
                    name, 
                    sub_cat_menu, 
                    (
                        (name, categories[name]["link"]),
                        categories[name]["categories"],
                    )
                ]
            )

        else:

            menu.items.append(
                [
                    name,
                    category_link,
                    (name, categories[name]["link"])
                ]
            )
    
    menu.items += ['', ["Return", return_break]]

    menu.commit()

    while True:
        result = menu.show()
        if result:
            return result
        
def or_search(query):
    search_results = api.search(query)
    if not search_results:
        print(f" {red}No apps found!{reset}")
        press_enter()
        return "Break"

    results = search_results.results
    ordered_results = {}

    for i, result in enumerate(results.keys(), start=1):
        ordered_results[str(i)] = result

    tui.clean()

    while True:
        tui.clean()
        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        print(" │         ╔══════════════════╗         │")
        print(" │         ║  Search results: ║         │")
        print(" │         ╚══════════════════╝         │")
        print(" │                                      │")
        for i, pkg in ordered_results.items():
            pkg = re.sub("\_\d+.+", "", pkg)
            _result = f"{i}. {pkg}"
            lenght = " " * int((38 - 2 - len(_result)))
            print(f" │  {_result}{lenght}│")
        print(" │                                      │")
        print(" │  0. Return                           │")
        print(" │                                      │")
        print(" └──────────────────────────────────────┘\n")
        ask = input(f"{yellow} Type numbers, ALL or 0:{reset} ")
        print()
        
        if not ask.isnumeric():
            print(f" {red}Wrong number, select a correct one!{reset}")
            print(" ")
            continue

        todl = ask.split(" ")
        todl = list(set(todl))
        todl = sorted([int(x) for x in todl if x.isdigit()])
        todl = list(map(str, todl))

        if not ask:
            continue
        if ask == "0":
            return
        if not all(num in ordered_results.keys() for num in todl):
            print(f" {red}Wrong number, select a correct one!{reset}")
            print(" ")
            continue
        i = todl[0]
        link = results[ordered_results.get(i)]['link']
        while True:
            _ = or_app(link=link)
            if _ == "Break":
                break
        tui.clean()