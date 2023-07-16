#!/usr/bin/python3.1

import os
import sys
import subprocess
sys.path.append("/opt/MeeShop/functions")
import dbc
from clean import clean

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def press_enter_to_exit():
    input(" {}{}Press Enter to exit... {}".format(blink, cyan, reset))
    sys.exit(1)

def main():

    clean()

    print(" Setting up workspace...\n")

    try:
        #folder = "."
        folder = "/opt/MeeShop/.cache"
        if not os.path.isdir(folder):
            if os.path.isfile(folder):
                os.remove(folder)
            os.mkdir(folder)
    
        os.chdir(folder)

    except:
        print(" {}Error while setting workspace...\n{}".format(red, reset))
        press_enter_to_exit()
    else:
        print(" {}Done!\n{}".format(green, reset))

    print(" Testing internet connection...\n")
    _ = subprocess.call("ping wunderwungiel.pl -c 1 > /dev/null 2>&1", shell=True)
    if _ != 0:
        print(" {}Failed to connect, check your internet connection.\n{}".format(red, reset))
        press_enter_to_exit()
    else:
        print(" {}Done!\n{}".format(green, reset))
    
    print(" Building databases...\n")

    db_creator = dbc.Db_creator()

    if db_creator.error:
        print(" {}Failed building databases...\n{}".format(red, reset))
        press_enter_to_exit()
    else:
        print(" {}Done!\n{}".format(green, reset))

    for f in os.listdir("."):
        if f.endswith(".deb"):
            os.remove(f)

    print(" Checking for Aegis-hack...\n")

    if not os.path.isfile("/usr/bin/aegis-apt-get"):
        print(" {}Aegis-install hack by CODeRUS needs to be installed.{}".format(red, reset))
        print(" Get it here:")
        print(" http://wunderwungiel.pl/MeeGo/apt-repo/pool/main/hack-installer_1.0.10_armel.deb")
        print(" ")
        press_enter_to_exit()

    else:
        print(" {}Done!\n{}".format(green, reset))

    print(" Importing necessary modules...\n")

    try:
        from first_menu import first_menu
        import apt
    except ImportError:
        print(" {}Failed importing necessary modules...\n{}".format(red, reset))
        press_enter_to_exit()
    else:
        print(" {}Done!\n{}".format(green, reset))

    print(" Testing dpkg lock state...\n")

    result = apt.is_dpkg_locked()
    if result:
        print(" {}dpkg / apt-get is busy and locked...{}".format(red, reset))
        print(" Close all dpkg / apt-get processes")
        print(" and try again. You can also reboot phone.\n")
        press_enter_to_exit()
    else:
        print(" {}Done!\n{}".format(green, reset))


    if not apt.is_repo_enabled():

        print(" Adding MeeShop repository...\n")

        result = apt.add_repo()

        if result == "Error":
            print(" {}Failed adding repository...\n{}".format(red, reset))
            press_enter_to_exit()
        else:
            print(" {}Done!\n{}".format(green, reset))

        print(" Updating repositories...\n")
        
        result = apt.update()

        if result == "Error":
            print(" {}Error updating repositories...{}".format(red, reset))
            press_enter_to_exit()
        else:
            print(" {}Done!\n{}".format(green, reset))

    while True:
        first_menu()
        clean()

if __name__ == "__main__":
    main()