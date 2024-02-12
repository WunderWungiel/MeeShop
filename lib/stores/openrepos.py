from .. import tui
from ..tui import Item, TUIMenu
from .. import api
from .. import apt
from .. small_libs import red, reset, press_enter, download_file, blink, cyan
import subprocess
import time

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

class OptionsActions:
    def files(self, files):

        def get_file(file, link):
            items = [
                Item('Download', download_file, (link, ".", file)),
                Item('Download with browser', app_options_actions.open_with_browser, link),
                '',
                Item('Return', returns=True)
            ]

            menu = TUIMenu(items=items, text=file)

            return menu

        menu = TUIMenu(text="Files", space_left=9, paged=True, items_on_page=10, repeat=-1)

        for file, link in files.items():
            file = file.strip()
            menu.items.append(
                Item(
                    file, 
                    get_file,
                    (file, link),
                    menu=True
                )
            )
        menu.items += Item("Return", returns=True)

        return menu

    def description(self, description):
        
        description = "\n".join([" " + line for line in description.splitlines()])
        print(description)
        print()
        press_enter()
        
options_actions = OptionsActions()

def or_app(link):
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

    lenght = " " * int((38 - 12 - len(maintainer)))
    custom_text += f"""
 │  Uploader: {maintainer}{lenght}│
 │                                      │"""

    menu = TUIMenu(custom_text=custom_text)

    menu.items = [
        Item('Files', options_actions.files, app_info.files, menu=True),
        Item('Description', options_actions.description, app_info.description),
        '',
        Item('Return', returns=True)
    ]

    return menu

def category_link(name, link):
    pass

def sub_cat_menu(main_cat, sub_categories):
    menu = TUIMenu()
        
    menu.items.append(
        Item(
            main_cat[0],
            category_link,
            (main_cat[0], main_cat[1])
        )
    )

    for name in sub_categories.keys():

        menu.items.append(
            Item(
                name,
                category_link,
                [name, sub_categories[name]]
            )
        )

    menu.items += ('', Item("Return", returns=True))
    
    return menu

categories = api.get_categories()
categories_menu = TUIMenu()

for name in categories.keys():

    if "categories" in categories[name]:
            
        categories_menu.items.append(
            Item(
                name, 
                sub_cat_menu, 
                (
                    (name, categories[name]["link"]),
                    categories[name]["categories"],
                ),
                menu=True
            )
        )

    else:

        categories_menu.items.append(
                Item(
                    name,
                    category_link,
                    (name, categories[name]["link"])
                )
            )
    
categories_menu.items += ['', Item("Return", returns=True)]

def or_search(query):

    search_results = api.search(query)
    if not search_results:
        print(f" {red}No apps found!{reset}")
        press_enter()
        return "break"

    results = search_results.results

    menu = TUIMenu(text="Search results", paged=True, items_on_page=10, repeat=-1)

    for result, properties in results.items():

        menu.items.append(
            Item(
                result,
                or_app,
                properties.get("link"),
                menu=True
            )
        )

    menu.items += [
        Item('Return', returns=True)
    ]

    menu.commit()

    while True:
        result = menu.show()
        if result == "break":
            return result