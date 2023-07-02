import sys
sys.path.append("functions")
from clean import clean

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def about():

    clean()

    print(" ┌──────────────────────────────────────┐")
    print(" │                                      │")
    print(" │      MeeShop© 2023 WunderWungiel     │")
    print(" │            Version: 0.1.1            │")
    print(" │                                      │")
    print(" │      App store for MeeGo Harmattan   │")
    print(" │      written using Python 3.1.       │")
    print(" │                                      │")
    print(" │      Special thanks to:              │")
    print(" │                                      │")
    print(" │        - IarChep                     │")
    print(" │      (icon, inexhaustible help       │")
    print(" │       and ingenuity!)                │")
    print(" │        - Python                      │")
    print(" │        - tqdm developers             │")
    print(" │        - LM World community          │")
    print(" │                                      │")
    print(" │      Join our Telegram group:        │")
    print(" │                                      │")
    print(" │    https://t.me/linuxmobile_world    │")
    print(" │                                      │")
    print(" └──────────────────────────────────────┘ \n")
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
    clean()