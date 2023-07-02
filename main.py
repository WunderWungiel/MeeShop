#!/usr/bin/python3.1

import os
from urllib.request import urlopen
import sys
from urllib.error import HTTPError, URLError

from functions.clean import clean
from functions.first_menu import first_menu
import functions.dbc as dbc

db_creator = dbc.Db_creator()

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def main():

    clean()

    folder = "."
    #folder = "/opt/MeeShop/.cache"
    if not os.path.isdir(folder):
        if os.path.isfile(folder):
            os.remove(folder)
        os.mkdir(folder)
    
    os.chdir(folder)

    try:
        urlopen("http://wunderwungiel.pl")
    except (HTTPError, URLError):
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

    while True:
        first_menu()
        clean()

if __name__ == "__main__":
    main()