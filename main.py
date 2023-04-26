#!/usr/bin/python3

import os
from urllib.request import urlopen
import sys
import subprocess
from xml.etree import ElementTree as ET

from functions.clean import clean
from functions.category import category
import functions.category
import functions.search
import functions.options

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

    _ = subprocess.call("ping wunderwungiel.pl -c 2 > /dev/null 2>&1", shell=True)
    if _ != 0:
        print(" {}Failed to connect, please\n check your internet connection.{}".format(red, reset))
        print()
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        clean()
        sys.exit(1)

    for f in os.listdir("."):
        if f.endswith(".deb"):
            os.remove(f)

    if not os.path.exists("/usr/bin/aegis-apt-get"):
        print(" {}Aegis-install hack by CODeRUS needs to be installed.{}".format(red, reset))
        print(" Get it here:")
        print(" http://wunderwungiel.pl/MeeGo/apt-repo/pool/main/hack-installer_1.0.10_armel.deb")
        print(" ")
        sys.exit(1)

    r = urlopen("http://wunderwungiel.pl/MeeGo/openrepos/catalog.xml")
    with open("catalog.xml", "w") as f:
        f.write(r.read().decode("utf-8"))

    r= urlopen("http://wunderwungiel.pl/MeeGo/.database/Ovi.txt")
    with open("Ovi.txt", "w") as f:
        f.write(r.read().decode("utf-8"))
    with open("Ovi.txt", "r") as f:
        ovi_db = f.readlines()

    tree = ET.parse('catalog.xml')
    root = tree.getroot()

    db = {}

    for app in root.findall('app'):
        package = app.find('data').get('package')
        display_name = app.find('data').get('name')
        developer = app.find('data').get('dev')
        version = app.find('data').get('ver')
        file = app.find('data').get('deb')
        size = app.find('data').get('size')
    
        db[package] = {
            'file': file,
            'version': version,
            'developer': developer,
            'package': package,
            'display_name': display_name,
            'size': size
        }

    functions.category.init(db)
    functions.search.init(_ovi_db=ovi_db)
    functions.options.init()

    while True:
        category()
        clean()

if __name__ == "__main__":
    main()