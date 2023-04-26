import re
from urllib.parse import quote
import subprocess
import time

from .clean import clean
from .apt import Apt

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def init(_ovi_db):
    global apt
    global ovi_db
    ovi_db = _ovi_db
    apt = Apt()

class Search:
    
    def app(self, package, db):
    
        clean()

        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        display_name = db[package]['display_name']
        if len(display_name) % 2 != 0:
            display_name = display_name + " "
        lenght = " " * int((38 - len(display_name)) / 2)
        print(" │{}{}{}│".format(lenght, display_name, lenght))

        print(" │                                      │")
    
        lenght = " " * int((38 - 13 - len(package)))
        print(" │  Package: {} ✓{}│".format(package, lenght))

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

        filename = db[package]['file']
    
        link = "MeeGo/openrepos/" + db[package]['file']
        link = quote(link)
        link = "http://wunderwungiel.pl/" + link

        if apt.is_installed(package):
            print(" │      1. Uninstall                    │")
        else:
            print(" │      1. Download & install           │")
            print(" │      2. Download                     │")
        print(" │      3. Open with browser            │")
        print(" │                                      │")
        print(" │      0. Return                       │")
        print(" │                                      │")
        print(" └──────────────────────────────────────┘\n")

        while True:
            category = input(" ")
            print()
            if not category:
                continue
            if not category.isnumeric() or int(category) not in [1, 2, 3, 0]:
                continue
            else:
                category = int(category)
                break
        if category == 1:
        
            if apt.is_installed(package):
                apt.uninstall(package)
            else:
                apt.download(file=filename, prompt=False)
                apt.install(display_name=display_name, filename=filename)

        elif category == 2:

            apt.download(file=filename, prompt=True, mydocs=True)
            input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

        elif category == 3:
            subprocess.Popen("/usr/bin/invoker --type=m /usr/bin/grob {} > /dev/null 2>&1".format(link), shell=True)
            time.sleep(1.5)
            input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        elif category == 0:
            return "Break"

    def ovi_app(self, file, link):
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
            if not category.isnumeric() or int(category) not in [1, 2, 0]:
                continue
            else:
                category = int(category)
                break
        if category == 1:
        
            apt.ovi_download(file="{}_armel.deb".format(file), link=link, prompt=False)
            apt.install(display_name="{}_armel.deb".format(file), filename="{}_armel.deb".format(file))

        elif category == 2:

            apt.ovi_download(file="{}_armel.deb".format(file), link=link, prompt=True, mydocs=True)
            input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        elif category == 0:
            return "Break"

    def ovi_search(self, query):

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
                _ = self.ovi_app(file=file, link=links[file])
                if _ == "Break":
                    break
            clean()

    def search(self, db, query):

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
                _ = self.app(package=package, db=db)
                if _ == "Break":
                    break
            clean()