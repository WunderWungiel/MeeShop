import re
import sys

from .clean import clean
from .options import options
from .aptfixer import apt_fixer
from .rss import rss
from .about import about
from .language import language

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

def category():

    while True:
        clean()
        strings.category_selection_list()
        supported = range(0, 8)
        category = input(" ")
        print()
        if not category:
            clean()
            continue
        if not category.isnumeric() or int(category) not in supported:
            continue
        else:
            break
    
    if category == "1":
        db_name = "apps.txt"
        addr = "Applications"
        name = strings.categories.applications()
    elif category == "2":
        db_name = "games.txt"
        addr = "Games"
        name = strings.categories.games()
    elif category == "3":
        db_name = "personalisation.txt"
        addr = "Personalisation"
        name = strings.categories.personalisation()
    elif category == "4":
        rss()
        clean()
        return
    elif category == "5":
        apt_fixer()
        clean()
        return
    
    elif category == "6":
        language()
        clean()
        return

    elif category == "7":
        about()
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
        _ = options(db, addr, name)
        if _ == "Break":
            clean()
            break 