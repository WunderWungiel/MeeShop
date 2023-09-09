#!/usr/bin/python3.1

import os
import sys
import subprocess
import lib.dbc as dbc
import lib.tui as tui

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

rprint = tui.rprint

def press_enter_to_exit():
    input(" {}{}Press Enter to exit... {}".format(blink, cyan, reset))
    sys.exit(1)

def main():

    tui.clean()

    rprint(" Setting up workspace...")

    try:
        folder = "."
        #folder = "/opt/MeeShop/.cache"
        if not os.path.isdir(folder):
            if os.path.isfile(folder):
                os.remove(folder)
            os.mkdir(folder)
    
        os.chdir(folder)

    except:
        rprint("{} Error while setting workspace...{}".format(red, reset))
        press_enter_to_exit()
    else:
        rprint("{} Done!{}".format(green, reset))

    rprint(" Testing internet connection...")
    result = subprocess.call("ping wunderwungiel.pl -c 1 > /dev/null 2>&1", shell=True)
    if result != 0:
        rprint("{} Failed to connect, check your internet connection.{}".format(red, reset))
        press_enter_to_exit()
    else:
        rprint("{} Done!{}".format(green, reset))
    
    rprint(" Building databases...")

    db_creator = dbc.Db_creator()

    if db_creator.error:
        rprint("{} Failed building databases...{}".format(red, reset))
        press_enter_to_exit()
    else:
        rprint("{} Done!{}".format(green, reset))

    for f in os.listdir("."):
        if f.endswith(".deb"):
            os.remove(f)

    rprint(" Checking for Aegis-hack...")

    """if not os.path.isfile("/usr/bin/aegis-apt-get"):
        rprint("{} Aegis-install hack by CODeRUS needs to be installed.{}".format(red, reset), _end='\n')
        rprint(" Get it here:", _end='\n')
        rprint(" http://wunderwungiel.pl/MeeGo/apt-repo/pool/main/hack-installer_1.0.10_armel.deb", _end='\n')
        rprint(" ", _end='\n')
        press_enter_to_exit()

    else:
        rprint("{} Done!{}".format(green, reset))"""

    rprint(" Importing necessary modules...")

    try:
        from lib.first_menu import first_menu
        import lib.apt as apt
    except ImportError:
        rprint("{} Failed importing necessary modules...{}".format(red, reset))
        press_enter_to_exit()
    else:
        rprint("{} Done!{}".format(green, reset))

    rprint(" Testing dpkg lock state...")

    result = apt.is_dpkg_locked()
    if result:
        rprint("{} dpkg / apt-get is busy and locked...{}".format(red, reset), end='\n')
        rprint(" Close all dpkg / apt-get processes", end='\n')
        rprint(" and try again. You can also reboot phone.")
        press_enter_to_exit()
    else:
        rprint("{} Done!{}".format(green, reset))


    """if not apt.is_repo_enabled():
        
        rprint(" Adding MeeShop repository...\n")

        result = apt.add_repo()

        if result == "Error":
            rprint("{} Failed adding repository...{}".format(red, reset))
            press_enter_to_exit()
        else:
            rprint("{} Done!{}".format(green, reset))

        rprint(" Updating repositories...")
        
        result = apt.update()

        if result == "Error":
            rprint("{} Error updating repositories...{}".format(red, reset))
            press_enter_to_exit()
        else:
            rprint("{} Done!{}".format(green, reset))"""

    while True:
        first_menu()
        tui.clean()

if __name__ == "__main__":
    main()