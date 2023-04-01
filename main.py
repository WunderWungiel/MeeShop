#!/usr/bin/python3

import os
from urllib.request import urlopen
import sys
import subprocess
import re

from functions.clean import clean
from functions.category import category
import functions.about
import functions.aptfixer
import functions.category
import functions.language
import functions.options
import functions.rss
import functions.search

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def main():

    clean()

    #folder = "."
    folder = "/opt/MeeShop/.cache"
    if not os.path.isdir(folder):
        if os.path.isfile(folder):
            os.remove(folder)
        os.mkdir(folder)
    
    os.chdir(folder)

    if os.path.isfile(".config"):
        with open(".config", "r") as f:
            lang = re.search("lang = (.{2})", f.read())
            if lang:
                lang = lang.group(1)
        if not lang in ["en", "ru"]:
            lang = "en"
            with open(".config", "w") as f:
                f.write("lang = en")
    else:
        with open(".config", "w") as f:
            f.write("lang = en")
        lang = "en"

    if lang == "en":
        from langs.en import Strings
    elif lang == "ru":
        from langs.ru import Strings

    strings = Strings()

    functions.about.init(lang)
    functions.aptfixer.init(lang)
    functions.category.init(lang)
    functions.language.init(lang)
    functions.options.init(lang)
    functions.rss.init(lang)
    functions.search.init(lang)

    _ = subprocess.call("ping wunderwungiel.pl -c 2 > /dev/null 2>&1", shell=True)
    if _ != 0:
        strings.something_wrong_with_internet_connection()
        print()
        strings.press_enter_to_continue()
        clean()
        sys.exit(1)

    for f in os.listdir("."):
        if f.endswith(".deb"):
            os.remove(f)

    if not os.path.exists("/usr/bin/aegis-apt-get"):
        strings.aegis_hack_not_found()
        print(" http://wunderwungiel.pl/MeeGo/apt-repo/pool/main/hack-installer_1.0.10_armel.deb")
        print(" ")
        sys.exit(1)
    
    for db_name in ["apps.txt", "games.txt", "personalisation.txt"]:
        with urlopen("http://wunderwungiel.pl/MeeGo/.database/{}".format(db_name)) as response:
            _db = response.read().decode("utf-8")
        with open(db_name, "w") as f:
            f.write(_db)

    while True:
        category()
        clean()

if __name__ == "__main__":
    main()