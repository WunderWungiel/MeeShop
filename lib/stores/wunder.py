import subprocess
import time
from urllib.parse import quote

from ..small_libs import red, reset, blink, cyan, yellow, re_decoder, press_enter, download_file
from .. import apt
from .. import tui
from ..tui import TUIMenu, Item
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
    
app_options_actions = AppOptionsActions()

def ask_for_search(category):
    tui.clean()
    tui.frame(text="Search:")
    query = input(f"{yellow} Query to search:{reset} ")
    if not query or query == "0":
        return "break"
    else:
        query = re_decoder(query)
        search(query=query, category=category)

def search(query, category="full"):

    our_db = categories[category]["db"]

    search_menu = TUIMenu(text="Search results")

    results = []

    for dict in our_db.values():
        if query.lower() in dict['display_name'].lower():
            results.append(dict['display_name'])

    if len(results) == 0:
        print(f" {red}No apps found!{reset}")
        press_enter()
        return "break"

    for result in results:
        for key, value in our_db.items():
            if value['display_name'] == result:
                search_menu.items.append(
                    Item(
                        result,
                        app,
                        key,
                        menu=True
                    )
                )

    search_menu.items.append(
        Item("Return", returns=True)
    )
    
    search_menu.commit()

    return search_menu

def app(package):
    
    db = categories["full"]["db"]

    tui.clean()

    icon = db[package]['icon']
    if icon:
        download_file("http://wunderwungiel.pl/MeeGo/openrepos/icons/" + icon, folder="icons", filename=icon, log=False)
        process = subprocess.run(["viu", f"icons/{icon}", "-h", "3", "-b"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        icon_list = process.stdout.splitlines()

        icon = ""

        for i, line in enumerate(icon_list):
            if i == 0:
                icon += f" │                {line}                │"
            else:
                icon += f"\n │                {line}                │"
    
        custom_text = icon
    else:
        custom_text = ''


    display_name = db[package]['display_name']
    if len(display_name) % 2 != 0:
        display_name = display_name + " "
    lenght = " " * int((38 - len(display_name)) / 2)
    custom_text += f"""
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
            Item('Uninstall', app_options_actions.uninstall, package),
            Item('Download', app_options_actions.download, package),
            Item('Download with browser', app_options_actions.open_with_browser, link),
            '',
            Item('Return', returns=True)
        ]

    else:

        items = [
            Item('Install', app_options_actions.download_install, package),
            Item('Download', app_options_actions.download, package),
            Item('Download with browser', app_options_actions.open_with_browser, link),
            '',
            Item('Return', returns=True)
        ]

    menu = TUIMenu(items=items, custom_text=custom_text)

    return menu

def show_apps(category="full"):

    our_db = categories[category]["db"]

    numbers = []
    db_list = []

    for i, pkg in enumerate(our_db.keys(), start=1):
        numbers.append(str(i))
        db_list.append(pkg)

    menu = TUIMenu(paged=True, repeat=-1)

    for pkg in db_list:
        menu.items.append(
            Item(
                pkg,
                app,
                pkg,
                menu=True
            )
        )

    menu.items.append(Item('Return', returns=True))
    
    return menu