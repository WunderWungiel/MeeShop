import re

from .. import tui
from ..tui import TUIMenu, Item
from .. import apt
from ..small_libs import quit, red, reset, cyan, blink, yellow, download_file, press_enter
from ..dbc import ovi_db

class OviAppOptionsActions:
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
        
ovi_app_options_actions = OviAppOptionsActions()

def ovi_app(file, link):
    menu = TUIMenu()

    menu.text = file.replace("_armel.deb", '')
    
    menu.items = [
        Item('Download & install', ovi_app_options_actions.download_install, [file, link]),
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
        menu.items.append(
            Item(
                file.replace("_armel.deb", ""),
                ovi_app,
                (file, link),
                menu=True
            )
        )

    menu.items += [
        '',
        Item("Return", returns=True)
    ]

    return menu