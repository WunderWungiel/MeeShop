#!/usr/bin/python3

import os
from urllib.request import urlopen
import sys
import subprocess

from functions.clean import clean
from functions.category import category

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def main():

    clean()

    _ = subprocess.call("ping wunderwungiel.pl -c 2 > /dev/null 2>&1", shell=True)
    if _ != 0:
        print(" {}Something wrong with internet connection.{}".format(red, reset))
        print()
        input(" {}{}Press any key to continue... {}".format(blink, cyan, reset))
        clean()
        sys.exit(1)

    #folder = "."
    folder = "/opt/MeeShop/.cache"
    if not os.path.isdir(folder):
        if os.path.isfile(folder):
            os.remove(folder)
        os.mkdir(folder)
    
    os.chdir(folder)

    for f in os.listdir("."):
        if f.endswith(".deb"):
            os.remove(f)

    if not os.path.exists("/usr/bin/aegis-apt-get"):
        print(" {}Aegis-install hack by CODeRUS needs to be installed.{}".format(red, reset))
        print(" Get it here:")
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