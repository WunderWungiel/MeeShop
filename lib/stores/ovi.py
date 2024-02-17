import re

from ..tui import TUIMenu, Item
from .. import apt
from ..small_libs import quit, red, reset, cyan, blink, download_file, press_enter, send_notification
from ..dbc import ovi_db

class OviAppOptionsActions:
    def download_install(self, name, file, link):
        print(file, link)
        download_file(filename=file, link=link, prompt=False)
        try:
            apt.dpkg_install(display_name=name, filename=file)
        except Exception as e:
            print(f" Error {red}{e}{reset}! Report to developer.")
            input(f"{blink}{cyan} Press Enter to exit... {reset}")
            quit(1)
        else:
            send_notification(title="MeeShop (Ovi)", text=f"{name} installed!", icon="/usr/share/icons/hicolor/80x80/apps/MeeShop80.png")
    def download(self, file, link):
        download_file(filename=file, link=link, prompt=True, folder="/home/user/MyDocs")
        press_enter()
        
ovi_app_options_actions = OviAppOptionsActions()

def ovi_app(name, file, link):
    menu = TUIMenu()

    menu.text = file.replace("_armel.deb", '')
    
    menu.items = [
        Item('Download & install', ovi_app_options_actions.download_install, [name, file, link]),
        Item('Download', ovi_app_options_actions.download, [file, link]),
        '',
        Item('Return', returns=True)
    ]

    return menu

def ovi_search(query):

    results = {}

    for line in ovi_db:
        file = re.search(f"(?i)\d+\/(.*{query}.*)\?", line)
        if file:
            file = file.group(1)
            results[file] = "http://web.archive.org/web/20150215101210id_/http://d.ovi.com/p/g/store/" + line

    if len(results) == 0:
        print(f" {red}No apps found!{reset}")
        press_enter()
        return "break"

    menu = TUIMenu(text="Search results:")

    for file, link in results.items():
        name = file.replace("_armel.deb", "")
        menu.items.append(
            Item(
                name,
                ovi_app,
                (name, file, link),
                menu=True
            )
        )

    menu.items += [
        '',
        Item("Return", returns=True)
    ]

    return menu