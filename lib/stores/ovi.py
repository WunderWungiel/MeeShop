import re

from .. import tui
from .. import apt
from ..small_libs import quit, red, reset, cyan, blink, yellow
from ..dbc import ovi_db

class OviAppOptionsActions:
    def __init__(self):
        pass
    def download_install(self, *args):
        file, link = args
        apt.ovi_download(file="{}_armel.deb".format(file), link=link, prompt=False)
        try:
            apt.ovi_install(display_name="{}_armel.deb".format(file), filename="{}_armel.deb".format(file))
        except Exception as e:
            print(" Error {}{}{}! Report to developer.".format(red, e, reset))
            input("{}{} Press Enter to exit... {}".format(blink, cyan, reset))
            quit(1)
    def download(self, *args):
        file, link = args
        apt.ovi_download(file="{}_armel.deb".format(file), link=link, prompt=True, mydocs=True)
        tui.press_enter()
    def exit(self):
        return "Break"
        
ovi_app_options_actions = OviAppOptionsActions()

def ovi_app(file, link):
    tui.clean()

    options = {
        'Download & install': ovi_app_options_actions.download_install,
        'Download': ovi_app_options_actions.download,
        'Return': ovi_app_options_actions.exit
    }

    args = {
        'Download & install': [file, link],
        'Download': [file, link]
    }

    text = file.replace(".deb", '')

    while True:
        tui.clean()
        result = tui.menu(options=options, text=text, args=args)
        if result:
            return result

def ovi_search(query):

    print()
    links = {}
    numbers = []
    results = []

    for line in ovi_db:
        file = re.search("(?i)\d+\/(.*{}.*)\?".format(query), line)
        if file:
            file = file.group(1)
            file = file.replace("_armel.deb", "")
            results.append(file)
            links[file] = "http://web.archive.org/web/20150215101210id_/http://d.ovi.com/p/g/store/" + line
    for i, result in enumerate(results, start=1):
        numbers.append(str(i))

    if len(results) == 0:
        print(" {}No apps found!{}".format(red, reset))
        tui.press_enter()
        return "Break"

    tui.clean()

    print()

    while True:
        tui.clean()
        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        print(" │         ╔══════════════════╗         │")
        print(" │         ║  Search results: ║         │")
        print(" │         ╚══════════════════╝         │")
        print(" │                                      │")
        for i, pkg in zip(numbers, results):
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
        if not all(num in numbers for num in todl):
            print(" {}Wrong number, select a correct one!{}".format(red, reset))
            print(" ")
            continue
        i = todl[0]
        file = results[numbers.index(i)]
        while True:
            _ = ovi_app(file=file, link=links[file])
            if _ == "Break":
                break
        tui.clean()