import re
import sys

from .clean import clean
from .options import options
from .aptfixer import apt_fixer
from .rss import rss

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def category():
    
    while True:
        clean()
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |         Welcome to {}MeeShop{}!          |".format(cyan, reset))
        print(" |                                      |")
        print(" |       {}Select category / option{}       |".format(blink, reset))
        print(" |                                      |")
        print(" |         1. Applications              |")
        print(" |         2. Games                     |")
        print(" |         3. Personalisation           |")
        print(" |                                      |")
        print(" |         4. RSS Feeds                 |")
        print(" |                                      |")
        print(" |         5. APT fixer                 |")
        print(" |                                      |")
        print(" |         0. Exit                      |")
        print(" |                                      |")
        print("  -------------------------------------- \n")
        supported = ["1", "2", "3", "4", "5", "0"]
        category = input(" ")
        print()
        if not category:
            clean()
            continue
        if category not in supported:
            print(" {}Wrong number, select a correct one!{}".format(red, reset))
            print(" ")
            continue
        else:
            break
    
    if category == "1":
        db_name = "apps.txt"
        addr = "Applications"
    elif category == "2":
        db_name = "games.txt"
        addr = "Games"
    elif category == "3":
        db_name = "personalisation.txt"
        addr = "Personalisation"
    elif category == "4":
        rss()
        clean()
        return
    elif category == "5":
        apt_fixer()
        clean()
        return
    else:
        clean()
        sys.exit(0)

    with open(db_name, 'r') as f:  # open file for reading
        lines = f.readlines()
    
    db = {}

    for line in lines:
        package = re.search("(.+) v\d", line)
        if package:
            package = package.group(1)
        version = re.search(".+ (v\d.+)", line)
        if package:
            version = version.group(1)

        db[package] = version

    while True:
        _ = options(db, addr)
        if _ == "Break":
            clean()
            break 