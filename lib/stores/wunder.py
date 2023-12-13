import subprocess
import time
from urllib.parse import quote

from ..small_libs import red, reset, blink, cyan, yellow, re_decoder, press_enter
from .. import apt
from .. import tui
from lib._tui.paged_menu import PagedMenu
from ..dbc import categories

class AppOptionsActions:
    def __init__(self):
        pass
    def download_install(self, package):
        try:
            apt.install(package)
        # apt-get wasn't able to install the package successfully.
        except Exception as e:
            print(f" Error {red}{e}{reset}! Report to developer.")
            input(f"{blink}{cyan} Press Enter to exit... {reset}")
    def download(self, package):
        apt.download(package)
        press_enter()
    def open_with_browser(self, link):
        subprocess.Popen(["/usr/bin/invoker", "--type=m", "/usr/bin/grob", link], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1.5)
        press_enter()
    def uninstall(self, package):
        try:
            apt.uninstall(package)
        except Exception as e:
            print(f" Error {red}{e}{reset}! Report to developer.")
            input(f"{blink}{cyan} Press Enter to exit... {reset}")
    def exit(self):
        return "Break"
    
app_options_actions = AppOptionsActions()

def ask_for_search(category):
    tui.clean()
    tui.frame(text="Search:")
    query = input(f"{yellow} Query to search:{reset} ")
    if not query:
        return "Break"
    if query == "0":
        return "Break"
    else:
        query = re_decoder(query)
        search(query=query, category=category)

def search(query, category="full"):

    our_db = categories[category]["db"]

    numbers = []
    results = []
    packages = {}

    for pkg, dict in our_db.items():
        if query.lower() in dict['display_name'].lower():
            results.append(dict['display_name'])
    for i, result in enumerate(results, start=1):
        numbers.append(str(i))

    if len(results) == 0:
        print(f" {red}No apps found!{reset}")
        press_enter()
        return "Break"

    for result in results:
        for key, value in our_db.items():
            if value['display_name'] == result:
                packages[value['display_name']] = key
    
    while True:
        tui.clean()
        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        print(" │         ╔══════════════════╗         │")
        print(" │         ║  Search results: ║         │")
        print(" │         ╚══════════════════╝         │")
        print(" │                                      │")

        for i, pkg in zip(numbers, results):
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

        todl = ask.split(" ")[0]

        if not ask:
            continue
        if ask == "0":
            return "Break"
        if not todl in numbers:
            print(f" {red}Wrong number, select a correct one!{reset}")
            print(" ")
            continue
        package = packages[results[numbers.index(todl)]]
        while True:
            _ = app(package=package)
            if _ == "Break":
                break
        tui.clean()

def app(package):
    
    db = categories["full"]["db"]

    tui.clean()

    process = subprocess.run(["viu", "/home/wunderwungiel/Pobrane/abplayer.png", "-h", "3", "-b"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    icon_list = process.stdout.splitlines()

    icon = ""

    for i, line in enumerate(icon_list):
        if i == 0:
            icon += f" │                {line}                │"
        else:
            icon += f"\n │                {line}                │"
    
    display_name = db[package]['display_name']
    if len(display_name) % 2 != 0:
        display_name = display_name + " "
    lenght = " " * int((38 - len(display_name)) / 2)
    
    custom_text = f"""{icon}
 │                                      │
 │{lenght}{display_name}{lenght}│
 │                                      │"""
    
    if apt.is_installed(package):
        lenght = " " * int((38 - 13 - len(package)))
        custom_text += f"\n │  Package: {package} ✓{lenght}│"
    else:
        lenght = " " * int((38 - 11 - len(package)))
        custom_text += f"\n │  Package: {package}{lenght}│"

    size = db[package]['size']

    lenght = " " * int((38 - 8 - len(size)))
    custom_text += f"\n │  Size: {size}{lenght}│"

    version = db[package]['version']

    lenght = " " * int((38 - 11 - len(version)))
    custom_text += f"\n │  Version: {version}{lenght}│"

    developer = db[package]['developer']

    lenght = " " * int((38 - 14 - len(developer)))
    custom_text += f"""
 │  Maintainer: {developer}{lenght}│
 │                                      │"""

    link = "MeeGo/openrepos/" + db[package]['file']
    link = quote(link)
    link = "http://wunderwungiel.pl/" + link

    if apt.is_installed(package):
        items = [
            ['Uninstall', app_options_actions.uninstall, package],
            ['Download', app_options_actions.download, package],
            ['Download with browser', app_options_actions.open_with_browser, link],
            '',
            ['Return', app_options_actions.exit]
        ]

    else:

        items = [
            ['Download & install', app_options_actions.download_install, package],
            ['Download', app_options_actions.download, package],
            ['Download with browser', app_options_actions.open_with_browser, link],
            '',
            ['Return', app_options_actions.exit]
        ]

    menu = tui.TUIMenu(items=items, custom_text=custom_text, space_left=6)

    menu.commit()

    while True:
        tui.clean()
        result = menu.show()
        if result:
            return result

def show_apps(category="full"):

    def show_app(package):
        while True:
            result = app(package)
            if result:
                break

    our_db = categories[category]["db"]

    numbers = []
    db_list = []

    for i, pkg in enumerate(our_db.keys(), start=1):
        numbers.append(str(i))
        db_list.append(pkg)

    menu = tui.TUIMenu(paged=True, repeat=-1)

    for pkg in db_list:
        menu.items.append(
            [
                pkg,
                show_app,
                pkg
            ]
        )

    menu.items.append(('Return', app_options_actions.exit))
    
    menu.commit()

    while True:
        result = menu.show()
        if result == "Break":
            return "Break"