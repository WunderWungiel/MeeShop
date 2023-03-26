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
        print(" {}No apps found!{}".format(red, reset))
        input(" \n {}{}Press any key to continue...{}".format(blink, cyan, reset))
        return "Break"
    clean()

    print()

    print("  -------------------------------------- ")
    print(" |                                      |")
    print(" |            Search results:           |")
    print(" |                                      |")
    for i, pkg in zip(numbers, results):
        _result = "{}. {}".format(i, pkg)
        lenght = " " * int((38 - 2 - len(_result)))
        print(" |  {}{}|".format(_result, lenght))
    print(" |                                      |")
    print("  -------------------------------------- \n")
    while True:
        ask = input(" {}Type numbers, ALL or 0:{} ".format(yellow, reset))
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
                print(" {}{}WAIT!{}{} Downloading...\n{}".format(red, blink, reset, red, reset))
                with urlopen(url) as response:
                    _content = response.read()
                with open(cleaner(filename), "wb") as f:
                    f.write(_content)
                print(" Saved {}!\n".format(filename))

            print(" Installing...")
            print(" ")
            for pkg in results:
                filename = "{} {}.deb".format(pkg, db[pkg])
                filename = cleaner(filename)
                filepath = os.path.join("/opt/MeeShop/.cache", filename)
                command = 'aegis-dpkg -i "{}" > /dev/null'.format(filepath)
                subprocess.call(command, shell=True)

                print(" ")
                print(" {}{} installed!{}".format(green, pkg, reset))

            print()
            input(" {}{}Press any key to continue... {}".format(blink, cyan, reset))
            clean()
            return "Break"
        
        if ask != "a" and not all(num in numbers for num in todl):
            print(" {}Wrong number, select a correct one(s)!{}".format(red, reset))
            print(" ")
            continue
        else:
            for i in todl:
                pkg = results[numbers.index(i)]
                filename = "{} {}.deb".format(pkg, db[pkg])
                url = "wunderwungiel.pl/MeeGo/Repository/{}/{}".format(addr, filename)
                url = "http://" + urllib.parse.quote(url)
                print(" {}{}WAIT!{}{} Downloading...\n{}".format(red, blink, reset, red, reset))
                with urlopen(url) as response:
                    _content = response.read()
                with open(cleaner(filename), "wb") as f:
                    f.write(_content)
                print(" Saved {}!\n".format(filename))

            for i in todl:
                pkg = results[numbers.index(i)]
                filename = "{} {}.deb".format(pkg, db[pkg])
                filename = cleaner(filename)
                filepath = os.path.join("/opt/MeeShop/.cache", filename)
                command = 'aegis-dpkg -i "{}" > /dev/null'.format(filepath)
                subprocess.call(command, shell=True)
                print(" ")
                print(" {}{} installed!{}".format(green, pkg, reset))

            print()
            input(" {}{}Press any key to continue... {}".format(blink, cyan, reset))
            clean()
            return "Break"
 
