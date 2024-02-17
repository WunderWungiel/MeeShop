from .. import tui
from ..tui import Item, TUIMenu
from .. import api
from .. import apt
from .. small_libs import red, reset, press_enter, download_file, blink, cyan, send_notification, open_file
import subprocess
import time

class AppOptionsActions:
    def __init__(self):
        pass
    def download_install(self, file, link, name):
        download_file(filename=file, link=link, prompt=False)
        try:
            apt.dpkg_install(display_name=name, filename=file)
        except Exception as e:
            print(f" Error {red}{e}{reset}! Report to developer.")
            press_enter()
        else:
            send_notification(title="MeeShop (OpenRepos)", text=f"{name} installed!", icon="/usr/share/icons/hicolor/80x80/apps/MeeShop80.png")
    
    def download(self, file, link):
        download_file(link=link, filename=file, folder="/home/user/MyDocs", prompt=True)
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

class OptionsActions:
    def files(self, files, name):

        def get_file(file, link, name):
            items = [
                Item('Download & install', app_options_actions.download_install, (file, link, name)),
                Item('Download', app_options_actions.download, (file, link)),
                Item('Download with browser', app_options_actions.open_with_browser, link),
                '',
                Item('Return', returns=True)
            ]

            menu = TUIMenu(items=items, text=file)

            return menu

        menu = TUIMenu(text=f"Files for {name}", space_left=9, paged=True, items_on_page=10, repeat=-1)

        for file, link in files.items():
            file = file.strip()
            menu.items.append(
                Item(
                    file, 
                    get_file,
                    (file, link, name),
                    menu=True
                )
            )
        
        menu.items.append(Item("Return", returns=True))

        return menu
    
    def screenshots(self, screenshots, title):

        def open_screenshot(link):
            filename = download_file(link, prompt=False, log=False)
            open_file(filename)

        if not screenshots:
            menu = TUIMenu(text=name)

            menu.items=[Item("No screenshots", None), "", Item("Return", returns=True)]

            return menu

        menu = TUIMenu(paged=True, text=title, repeat=-1)

        for i, link in enumerate(screenshots, start=1):

            menu.items.append(
                Item(
                    f"Screenshot {i}",
                    open_screenshot,
                    link
                )
            )

        menu.items.append(Item("Return", returns=True))

        return menu

    def description(self, description):
        
        description = "\n".join([" " + line for line in description.splitlines()])
        print(description)
        print()
        press_enter()
        
options_actions = OptionsActions()

def or_app(link):
    app_info = api.get_app_info(link)
    title, stars, icon = app_info.title, app_info.stars, app_info.icon

    if len(title) % 2 != 0:
        title = title + " "

    download_file(icon, folder="icons", filename="openrepos.png", log=False)
    process = subprocess.run(["viu", "icons/openrepos.png", "-h", "3", "-b"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    icon_list = process.stdout.splitlines()

    icon_string = ""

    for i, line in enumerate(icon_list):
        if i == 0:
            icon_string += f" │                {line}                │"
        else:
            icon_string += f"\n │                {line}                │"

    custom_text = icon_string + "\n"
    
    blank_line = tui.blank_line()

    if custom_text:
        custom_text += blank_line + "\n"
    custom_text += tui.frame_around_text(title) + "\n"
    
    custom_text += blank_line

    stars_string = ''
    for star_status in stars.values():
        if star_status == "on":
            # stars_string += "⭐"
            stars_string += "⋆"
        else:
            stars_string += " "

    custom_text += f"\n │  Rating: {stars_string}                       │"

    maintainer = app_info.author

    lenght = " " * int((38 - 12 - len(maintainer)))
    custom_text += f"""
 │  Uploader: {maintainer}{lenght}│
 │                                      │"""

    menu = TUIMenu(custom_text=custom_text)

    menu.items = [
        Item('Files', options_actions.files, (app_info.files, title), menu=True),
        Item('Screenshots', options_actions.screenshots, (app_info.screenshots, title), menu=True),
        Item('Description', options_actions.description, app_info.description),
        '',
        Item('Return', returns=True)
    ]

    return menu

def category_link(name, link):
    
    apps = api.get_site_apps(link, target="harmattan_app")
    if not apps:
        menu = TUIMenu(text=name)

        menu.items=[Item("No apps", None), "", Item("Return", returns=True)]

        return menu

    menu = TUIMenu()

    menu.text = name

    for name, properties in apps.items():

        menu.items.append(
            Item(
                name, or_app, properties["link"], menu=True
            )
        )

    menu.items += ["", Item("Return", returns=True)]

    return menu

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
                [name, sub_categories.get(name)],
                menu=True
            )
        )

    menu.items += ['', Item("Return", returns=True)]
    
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
                    (name, categories[name]["link"]),
                    menu=True
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

    menu.items.append(Item('Return', returns=True))

    menu.commit()

    while True:
        result = menu.show()
        if result == "break":
            return result