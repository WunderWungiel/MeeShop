#!/opt/wunderw/bin/python3.11

import os
import subprocess

from lib.tui import rprint
from lib.first_menu import first_menu
from lib.small_libs import quit, green, blink, cyan, reset, red, clean

# Defines a simple function to exit app, in case of error.
def press_enter_to_exit():
    input(f"{blink}{cyan} Press Enter to exit... {reset}")
    quit(1)

def main():

    clean()

    print(" Setting up workspace...\n")

    try:
        # An optional "." is provided, for testing app on PC.
        # In this case, just swap "#" between them.

        folder = "."
        #folder = "/opt/MeeShop/.cache"
        if not os.path.isdir(folder):
            if os.path.isfile(folder):
                os.remove(folder)
            os.mkdir(folder)

        os.chdir(folder)

    # Generic Exception would be raised in case of error.
    except Exception as e:
        print(f"{red} Error while setting workspace...(error: {e}{reset}\n")
        press_enter_to_exit()
    else:
        print("{} Done!{}\n".format(green, reset))

    print(" Testing internet connection...\n")
    result = subprocess.call(["ping", "gnu.org", "-c", "1"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Exit code of above command is different than 0 in case of error.
    if result != 0:
        print(f"{red} Failed to connect, check your internet connection.{reset}\n")
        press_enter_to_exit()
    else:
        print(f"{green} Done!{reset}\n")

    print(" Checking for Aegis-hack...")

    # /usr/bin/aegis-apt-get should not exist if Aegis-hack not installed.
    if not os.path.isfile("/usr/bin/aegis-apt-get"):
        print("{red} Aegis-install hack by CODeRUS needs to be installed.{reset}")
        print(" Get it here:")
        print(" http://wunderwungiel.pl/MeeGo/apt-repo/pool/main/hack-installer_1.0.10_armel.deb")
        press_enter_to_exit()

    else:
        rprint("{} Done!{}".format(green, reset))

    # Here we run the first menu in loop, and clean the screen after each execution.
    while True:
        first_menu()
        clean()

# Running the main() function.
if __name__ == "__main__":
    main()
