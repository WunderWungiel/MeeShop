import re
from urllib.parse import quote
import subprocess
import time
import sys
sys.path.append("functions")
from clean import clean
import apt
import dbc

db_creator = dbc.Db_creator()
ovi_db = db_creator.ovi_db
db = db_creator.db
full_db = db_creator.full_db
libs_db = db_creator.libs_db

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'
    
def app(package, _clean=True):
    
    if _clean:
        clean()

    print(" ┌──────────────────────────────────────┐")
    print(" │                                      │")
    display_name = db[package]['display_name']
    if len(display_name) % 2 != 0:
        display_name = display_name + " "
    lenght = " " * int((38 - len(display_name)) / 2)
    print(" │{}{}{}│".format(lenght, display_name, lenght))

    print(" │                                      │")

    if apt.is_installed(package):
        lenght = " " * int((38 - 13 - len(package)))
        print(" │  Package: {} ✓{}│".format(package, lenght))
    else:
        lenght = " " * int((38 - 11 - len(package)))
        print(" │  Package: {}{}│".format(package, lenght))

    size = db[package]['size']

    lenght = " " * int((38 - 8 - len(size)))
    print(" │  Size: {}{}│".format(size, lenght))

    version = db[package]['version']

    lenght = " " * int((38 - 11 - len(version)))
    print(" │  Version: {}{}│".format(version, lenght))

    developer = db[package]['developer']

    lenght = " " * int((38 - 14 - len(developer)))
    print(" │  Maintainer: {}{}│".format(developer, lenght))
    print(" │                                      │")
    
    file = db[package]['file']

    link = "MeeGo/openrepos/" + db[package]['file']
    link = quote(link)
    link = "http://wunderwungiel.pl/" + link

    if apt.is_installed(package):
        print(" │      1. Uninstall                    │")
        print(" │      2. Open with browser            │")

        functions = {
            '1': 'uninstall',
            '2': 'open_browser',
            '0': 'return'
        }

    else:
        print(" │      1. Download & install           │")
        print(" │      2. Download                     │")
        print(" │      3. Open with browser            │")

        functions = {
            '1': 'install',
            '2': 'download',
            '3': 'open_browser',
            '0': 'return'
        }

    print(" │                                      │")
    print(" │      0. Return                       │")
    print(" │                                      │")
    print(" └──────────────────────────────────────┘\n")

    while True:
        answer = input(" ")
        print()
        if not answer:
            continue
        if not answer.isnumeric() or answer not in functions.keys():
            continue
        else:
            break

    action = functions[answer]

    if action == "uninstall":
        
        apt.uninstall(package)

    elif action == "install":

        apt.download(package, prompt=False)
        apt.install(display_name, file)

    elif action == "download":

        apt.download(package, prompt=True, mydocs=True)
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

    elif action == "open_browser":
        subprocess.Popen("/usr/bin/invoker --type=m /usr/bin/grob {} > /dev/null 2>&1".format(link), shell=True)
        time.sleep(1.5)
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
    
    elif action == "return":
        return "Break"

def ovi_app(file, link):
    clean()

    print(" ┌──────────────────────────────────────┐")
    print(" │                                      │")
    if len(file) % 2 != 0:
        file = file + " "
    lenght = " " * int((38 - len(file)) / 2)
    print(" │{}{}{}│".format(lenght, file, lenght))

    print(" │                                      │")
    print(" │      1. Download & install           │")
    print(" │      2. Download                     │")
    print(" │                                      │")
    print(" │      0. Return                       │")
    print(" │                                      │")
    print(" └──────────────────────────────────────┘\n")

    while True:
        category = input(" ")
        print()
        if not category:
            continue
        if not category.isnumeric() or category not in ["1", "2", "0"]:
            continue
        else:
            break
    if category == "1":
        
        apt.ovi_download(file="{}_armel.deb".format(file), link=link, prompt=False)
        apt.install(display_name="{}_armel.deb".format(file), filename="{}_armel.deb".format(file))

    elif category == "2":

        apt.ovi_download(file="{}_armel.deb".format(file), link=link, prompt=True, mydocs=True)
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
    elif category == 0:
        return "Break"

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
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        return "Break"

    clean()

    print()

    while True:
        clean()
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
        ask = input(" {}Type numbers, ALL or 0:{} ".format(yellow, reset))
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
        clean()

def search(query):

    print()

    numbers = []
    results = []
    packages = {}

    for pkg, dict in db.items():
        if re.search("(?i){}".format(query), dict['display_name']):
            results.append(re.search("(.+)", dict['display_name']).group(0))
    for i, result in enumerate(results, start=1):
        numbers.append(str(i))

    if len(results) == 0:
        print(" {}No apps found!{}".format(red, reset))
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        return "Break"
    clean()

    print()


    for result in results:
        for key, value in db.items():
            if value['display_name'] == result:
                packages[value['display_name']] = key
    
    while True:
        clean()
        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        print(" │         ╔══════════════════╗         │")
        print(" │         ║  Search results: ║         │")
        print(" │         ╚══════════════════╝         │")
        print(" │                                      │")

        for i, pkg in zip(numbers, results):
            if apt.is_installed(packages[pkg]):
                _result = "{}. {} ✓ ".format(i, pkg)
                lenght = " " * int((38 - 2 - len(_result)))
                print(" │  {}{}│".format(_result, lenght))
            else:
                _result = "{}. {}".format(i, pkg)
                lenght = " " * int((38 - 2 - len(_result)))
                print(" │  {}{}│".format(_result, lenght))
        print(" │                                      │")
        print(" │  0. Return                           │")
        print(" │                                      │")
        print(" └──────────────────────────────────────┘\n")
        ask = input(" {}Type numbers, ALL or 0:{} ".format(yellow, reset))
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
            return "Break"
        if not all(num in numbers for num in todl):
            print(" {}Wrong number, select a correct one!{}".format(red, reset))
            print(" ")
            continue
        i = todl[0]
        package = packages[results[numbers.index(i)]]
        while True:
            _ = app(package=package)
            if _ == "Break":
                break
        clean()

def show_apps(category="apps"):

    dbs = {
        "apps": db,
        "full": full_db,
        "libs": libs_db
    }

    our_db = dbs[category]

    numbers = []
    db_list = []

    for i, pkg in enumerate(our_db.keys(), start=1):
        numbers.append(str(i))
        db_list.append(pkg)

    clean()
    print(" ┌──────────────────────────────────────┐")
    print(" │                                      │")
    print(" │         ╔════════════════════╗       │")
    print(" │         ║  List of packages: ║       │")
    print(" │         ╚════════════════════╝       │")
    print(" │                                      │")
    
    rang_first = 0
    rang_last = 10

    _break = None

    while True:
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

        while True:
            answer = input(" \nEnter to more, number to show app,\n N to exit: ")
            print()

            if answer == "":
                break
            elif answer.lower() in ["n", "no"]:
                _break = True
                break
            else:
                if not answer.isnumeric():
                    print("Answer should be number or Enter")
                    continue
                if answer not in numbers:
                    print("Wrong number")
                    continue

                while True:
                    _ = app(db_list[numbers.index(answer)], _clean=None)
                    if _ == "Break":
                        break
        if _break:
            _break = None
            break

    while True:
        answer = input(" Type number or Enter to return: ")

        if answer != "":
            if not answer.isnumeric():
                print("Answer should be number")
                continue
            if answer not in numbers:
                print("Wrong number")
                continue

            while True:
                _ = app(db_list[numbers.index(answer)])
                if _ == "Break":
                    break

