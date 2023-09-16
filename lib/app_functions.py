import re
from urllib.parse import quote
import subprocess
import time
import sys
from . import tui
from . import apt
from . import dbc
from .re_decoder import re_decoder

db_creator = dbc.Db_creator()
ovi_db = db_creator.ovi_db
categories = db_creator.categories

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

class Ovi_App_Options_Actions:
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
            sys.exit(1)
    def download(self, *args):
        file, link = args
        apt.ovi_download(file="{}_armel.deb".format(file), link=link, prompt=True, mydocs=True)
        tui.press_enter()
    def exit(self):
        return "Break"

class App_Options_Actions:
    def __init__(self):
        pass
    def download_install(self, package):
        try:
            apt.install(package)
        except Exception as e:
            print(" Error {}{}{}! Report to developer.".format(red, e, reset))
            input("{}{} Press Enter to exit... {}".format(blink, cyan, reset))
    def download(self, package):
        apt.download(package)
        tui.press_enter()
    def open_with_browser(self, link):
        subprocess.Popen("/usr/bin/invoker --type=m /usr/bin/grob {} > /dev/null 2>&1".format(link), shell=True)
        time.sleep(1.5)
        tui.press_enter()
    def uninstall(self, package):
        try:
            apt.uninstall(package)
        except Exception as e:
            print(" Error {}{}{}! Report to developer.".format(red, e, reset))
            input("{}{} Press Enter to exit... {}".format(blink, cyan, reset))
    def exit(self):
        return "Break"
        
ovi_app_options_actions = Ovi_App_Options_Actions()
app_options_actions = App_Options_Actions()

def ask_for_search(category):
    tui.clean()
    tui.frame(text="Search:")
    query = input("{} Query to search:{} ".format(yellow, reset))
    if not query:
        return "Break"
    if query == "0":
        return "Break"
    else:
        query = re_decoder(query)
        search(query=query, category=category)

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
        custom_text += "\n │  Package: {} ✓{}│".format(package, lenght)
    else:
        lenght = " " * int((38 - 11 - len(package)))
        custom_text += "\n │  Package: {}{}│".format(package, lenght)

    size = db[package]['size']

    lenght = " " * int((38 - 8 - len(size)))
    custom_text += "\n │  Size: {}{}│".format(size, lenght)

    version = db[package]['version']

    lenght = " " * int((38 - 11 - len(version)))
    custom_text += "\n │  Version: {}{}│".format(version, lenght)

    developer = db[package]['developer']

    lenght = " " * int((38 - 14 - len(developer)))
    custom_text += """
 │  Maintainer: {}{}│
 │                                      │""".format(developer, lenght)

    link = "MeeGo/openrepos/" + db[package]['file']
    link = quote(link)
    link = "http://wunderwungiel.pl/" + link

    if apt.is_installed(package):
        options = {
            'Uninstall': app_options_actions.uninstall,
            'Download': app_options_actions.download,
            'Download with browser': app_options_actions.open_with_browser,
            'Return': app_options_actions.exit
        }

        args = {
            'Uninstall': [package],
            'Download': [package],
            'Open with browser': [link]
        }

    else:
        options = {
            'Download & install': app_options_actions.download_install,
            'Download': app_options_actions.download,
            'Download with browser': app_options_actions.open_with_browser,
            'Return': app_options_actions.exit
        }

        args = {
            'Download & install': [package],
            'Download': [package],
            'Open with browser': [link]
        }

    while True:
        tui.clean()
        result = tui.menu(options=options, args=args, custom_text=custom_text, space_left=6)
        if result:
            return result

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

def search(query, category="full"):

    our_db = categories[category]["db"]

    numbers = []
    results = []
    packages = {}

    for pkg, dict in our_db.items():
        if re.search("(?i){}".format(query), dict['display_name']):
            results.append(re.search("(.+)", dict['display_name']).group(0))
    for i, result in enumerate(results, start=1):
        numbers.append(str(i))

    if len(results) == 0:
        print(" {}No apps found!{}".format(red, reset))
        tui.press_enter()
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

        todl = ask.split(" ")[0]

        if not ask:
            continue
        if ask == "0":
            return "Break"
        if not todl in numbers:
            print(" {}Wrong number, select a correct one!{}".format(red, reset))
            print(" ")
            continue
        package = packages[results[numbers.index(todl)]]
        while True:
            _ = app(package=package)
            if _ == "Break":
                break
        tui.clean()

def show_apps(category="full"):

    our_db = categories[category]["db"]

    numbers = []
    db_list = []

    for i, pkg in enumerate(our_db.keys(), start=1):
        numbers.append(str(i))
        db_list.append(pkg)

    tui.clean()
    print(" ┌──────────────────────────────────────┐")
    print(" │                                      │")
    print(" │         ╔════════════════════╗       │")
    print(" │         ║  List of packages: ║       │")
    print(" │         ╚════════════════════╝       │")
    print(" │                                      │")
    print(" │ (Se)arch                             │")
    
    rang_first = 0
    rang_last = 10

    proceeded = 0

    _break = None

    while True:

        left = (len(db_list) - proceeded)
        if left < 10:
            for i in range(-1, -left-1, -1):
                pkg = db_list[i]
                number = numbers[i]
                pkg_name = our_db[pkg]['display_name']
                text = " {}. {}".format(number, pkg_name)
                if len(text) % 2 != 0:
                    text += " "
                length = " " * int(38 - len(text))
                print(" │{}{}│".format(text, length))
            
            while True:
                answer = input("{} \nInsert umber to show app,\n 0 to exit:{} ".format(cyan, reset))
                print()

                if answer == "0":
                    _break = True
                    break
                elif answer.lower() == "se":
                    _ = ask_for_search(category)
                    answer = input("{} Return to menu (y / Enter)?{} ".format(cyan, reset))
                    if answer.lower() == "y":
                        return "Break"
                    else:
                        break
                else:
                    if not answer.isnumeric():
                        print(" {}Answer should be number or Enter{}".format(red, reset))
                        continue
                    if answer not in numbers:
                        print(" Wrong number".format(red, reset))
                        continue

                    while True:
                        _ = app(db_list[numbers.index(answer)])
                        if _ == "Break":

                            answer = input("{} Return to menu (y / Enter)?{} ".format(cyan, reset))
                            if answer.lower() == "y":
                                return "Break"
                            else:
                                break

        if _break:
            _break = None
            break

        for i in range(rang_first, rang_last):
            pkg = db_list[i]
            number = numbers[i]
            pkg_name = our_db[pkg]['display_name']
            
            text = " {}. {}".format(number, pkg_name)
            if len(text) % 2 != 0:
                text += " "
            length = " " * int(38 - len(text))
            print(" │{}{}│".format(text, length))
        rang_first += 10
        rang_last += 10
        proceeded += 10

        while True:
            answer = input("{} \nEnter to more, number to show app,\n 0 to exit:{} ".format(cyan, reset))
            print()

            if answer == "":
                break
            elif answer == "0":
                return "Break"
            
            elif answer.lower() == "se":
                _ = ask_for_search(category)
                answer = input("{} Return to menu (y / Enter)?{} ".format(cyan, reset))
                if answer.lower() == "y":
                    return "Break"
                else:
                    break

            else:
                if not answer.isnumeric():
                    print(" {}Answer should be number or Enter{}".format(red, reset))
                    continue
                if answer not in numbers:
                    print(" {}Wrong number{}".format(red,reset))
                    continue

                while True:
                    _ = app(db_list[numbers.index(answer)])
                    if _ == "Break":
                        answer = input("{} Return to menu (y / Enter)?{} ".format(cyan, reset))
                        if answer.lower() == "y":
                            return "Break"
                        else:
                            break
        if _break:
            _break = None
            break

    print(" {}Type number, 0 to return:{}\n".format(cyan, reset))

    while True:
        answer = input()

        if answer == "0":
            return "Break"

        elif answer.lower() == "se":
            _ = ask_for_search(category)
            answer = input("{} Return to menu (y / Enter)?{} ".format(cyan, reset))
            if answer.lower() == "y":
                return "Break"
            else:
                pass

        else:
            if not answer.isnumeric():
                print(" {}Answer should be number{}".format(red, reset))
                continue
            if answer not in numbers:
                print(" {}Wrong number{}".format(red, reset))
                continue

            while True:
                _ = app(db_list[numbers.index(answer)])
                answer = input("{} Return to menu (y / Enter)?{} ".format(cyan, reset))
                if answer.lower() == "y":
                    return "Break"
                else:
                    break

