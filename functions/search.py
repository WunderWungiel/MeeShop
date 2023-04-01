import re
import urllib
import os
from urllib.request import urlopen
import subprocess

from .cleaner import cleaner
from .clean import clean

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def init(lang):
    global strings
    if lang == "en":
        from langs.en import Strings
    elif lang == "ru":
        from langs.ru import Strings

    strings = Strings()

def search(db, query, addr):

    print()

    numbers = []
    results = []
    for pkg in db.keys():
        if re.search("(?i){}".format(query), pkg):
            results.append(re.search("(.+)", pkg).group(1))
    for i, result in enumerate(results, start=1):
        numbers.append(str(i))

    if len(results) == 0:
        strings.no_apps_found()
        strings.press_enter_to_continue()
        return "Break"
    clean()

    print()

    strings.search_results()
    for i, pkg in zip(numbers, results):
        _result = "{}. {}".format(i, pkg)
        lenght = " " * int((38 - 2 - len(_result)))
        print(" |  {}{}|".format(_result, lenght))
    print(" |                                      |")
    print("  -------------------------------------- \n")
    while True:
        ask = strings.ask_for_results()
        print()
        todl = ask.split(" ")
        todl = list(set(todl))
        todl = sorted([int(x) for x in todl if x.isdigit()])
        todl = list(map(str, todl))
        if not ask:
            continue
        if ask == "0":
            return "Break"
        if ask.lower() in ["a", "all"]:
            for pkg in results:
                filename = "{} {}.deb".format(pkg, db[pkg])
                url = "wunderwungiel.pl/MeeGo/Repository/{}/{}".format(addr, filename)
                url = "http://" + urllib.parse.quote(url)
                strings.wait_downloading()
                with urlopen(url) as response:
                    _content = response.read()
                with open(cleaner(filename), "wb") as f:
                    f.write(_content)
                strings.saved(filename)

            strings.installing()
            print(" ")
            for pkg in results:
                filename = "{} {}.deb".format(pkg, db[pkg])
                filename = cleaner(filename)
                filepath = os.path.join("/opt/MeeShop/.cache", filename)
                command = 'aegis-dpkg -i "{}" > /dev/null'.format(filepath)
                subprocess.call(command, shell=True)

                print(" ")
                strings.installed(pkg)

            print()
            strings.press_enter_to_continue()
            clean()
            return "Break"
        
        if ask != "a" and not all(num in numbers for num in todl):
            strings.wrong_number()
            print(" ")
            continue
        else:
            for i in todl:
                pkg = results[numbers.index(i)]
                filename = "{} {}.deb".format(pkg, db[pkg])
                url = "wunderwungiel.pl/MeeGo/Repository/{}/{}".format(addr, filename)
                url = "http://" + urllib.parse.quote(url)
                strings.wait_downloading()
                with urlopen(url) as response:
                    _content = response.read()
                with open(cleaner(filename), "wb") as f:
                    f.write(_content)
                strings.saved(filename)

            for i in todl:
                pkg = results[numbers.index(i)]
                filename = "{} {}.deb".format(pkg, db[pkg])
                filename = cleaner(filename)
                filepath = os.path.join("/opt/MeeShop/.cache", filename)
                command = 'aegis-dpkg -i "{}" > /dev/null'.format(filepath)
                subprocess.call(command, shell=True)
                print(" ")
                strings.installed(pkg)

            print()
            strings.press_enter_to_continue()
            clean()
            return "Break"
 
