import re

from .. import tui
from .. import api
from ..small_libs import red, reset, yellow

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

        options = {}
        args = {}
        for file, link in files.items():
            options[file] = files_options_actions.get_file
            args[file] = link
        options["Return"] = files_options_actions.exit
        while True:
            _ = tui.menu(options=options, text="Files", args=args, space_left=5)
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
    custom_text += """
 │  Maintainer: {}{}│
 │                                      │""".format(maintainer, lenght)

    options = {
        'Files': or_app_options_actions.files,
        'Description': or_app_options_actions.description,
        'Return': or_app_options_actions.exit
    }

    args = {
        'Files': [app_info.files],
        'Description': app_info.description
    }

    while True:
        tui.clean()
        result = tui.menu(options=options, custom_text=custom_text, args=args)
        if result:
            return result

def search(query):
    search_results = api.search(query)
    if not search_results:
        print(" {}No apps found!{}".format(red, reset))
        tui.press_enter()
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
            _result = "{}. {}".format(i, pkg)
            lenght = " " * int((38 - 2 - len(_result)))
            print(" │  {}{}│".format(_result, lenght))
        print(" │                                      │")
        print(" │  0. Return                           │")
        print(" │                                      │")
        print(" └──────────────────────────────────────┘\n")
        ask = input("{} Type numbers, ALL or 0:{} ".format(yellow, reset))
        print()
        
        if not ask.isnumeric():
            print(" {}Wrong number, select a correct one!{}".format(red, reset))
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
            print(" {}Wrong number, select a correct one!{}".format(red, reset))
            print(" ")
            continue
        i = todl[0]
        link = results[ordered_results.get(i)]['link']
        while True:
            _ = or_app(link=link)
            if _ == "Break":
                break
        tui.clean()