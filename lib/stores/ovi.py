import re

from .. import tui
from .. import apt
from ..small_libs import quit, red, reset, cyan, blink, yellow, download_file, press_enter
from ..dbc import ovi_db

class OviAppOptionsActions:
    def __init__(self):
        pass
    def download_install(self, file, link):
        download_file(file=f"{file}_armel.deb", link=link, prompt=False)
        try:
            apt.ovi_install(display_name=f"{file}_armel.deb", filename=f"{file}_armel.deb")
        except Exception as e:
            print(f" Error {red}{e}{reset}! Report to developer.")
            input(f"{blink}{cyan} Press Enter to exit... {reset}")
            quit(1)
    def download(self, file, link):
        download_file(filename=f"{file}_armel.deb", link=link, prompt=True, folder="/home/user/MyDocs")
        press_enter()
    def exit(self):
        return "Break"
        
ovi_app_options_actions = OviAppOptionsActions()

def ovi_app(file, link):
    tui.clean()

    menu = tui.TUIMenu()

    menu.text = file.replace(".deb", '')
    menu.items = [
        ['Download & install', ovi_app_options_actions.download_install, [file, link]],
        ['Download', ovi_app_options_actions.download, [file, link]],
        '',
        ['Return', ovi_app_options_actions.exit]
    ]

    menu.commit()

    while True:
        result = menu.show()
        if result:
            return result

def ovi_search(query):

    print()
    links = {}
    numbers = []
    results = []

    for line in ovi_db:
        file = re.search(f"(?i)\d+\/(.*{query}.*)\?", line)
        if file:
            file = file.group(1)
            file = file.replace("_armel.deb", "")
            results.append(file)
            links[file] = "http://web.archive.org/web/20150215101210id_/http://d.ovi.com/p/g/store/" + line
    for i, result in enumerate(results, start=1):
        numbers.append(str(i))

    if len(results) == 0:
        print(f" {red}No apps found!{reset}")
        press_enter()
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
        if not all(num in numbers for num in todl):
            print(f" {red}Wrong number, select a correct one!{reset}")
            print(" ")
            continue
        i = todl[0]
        file = results[numbers.index(i)]
        while True:
            _ = ovi_app(file=file, link=links[file])
            if _ == "Break":
                break
        tui.clean()