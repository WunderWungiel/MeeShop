"""Copyright 2023 Wunder Wungiel

Small functions, that do not need additional files for each of them."""
import subprocess

bold = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'
cyan_background = '\033[48;5;104m'

# A very simple function, which just runs clear command.
# cls can be used on Windows instead.
def clean():
    subprocess.call(["clear"])

# A direct replacement for sys.exit(status_code)
# This way doesn't require to import sys, and does exactly the same.
def quit(status_code):
    raise SystemExit(status_code)

def about():

    print(" ┌──────────────────────────────────────┐")
    print(" │                                      │")
    print(" │      MeeShop© 2023 WunderWungiel     │")
    print(" │            Version: 0.3.0            │")
    print(" │                                      │")
    print(" │      App store for MeeGo Harmattan   │")
    print(" │      written using Python 3          │")
    print(" │                                      │")
    print(" │      Special thanks to:              │")
    print(" │                                      │")
    print(" │        - IarChep                     │")
    print(" │      (icon, inexhaustible help       │")
    print(" │       and ingenuity!)                │")
    print(" │        - Python                      │")
    print(" │        - LM World community          │")
    print(" │                                      │")
    print(" │      Join our Telegram group:        │")
    print(" │                                      │")
    print(" │    https://t.me/linuxmobile_world    │")
    print(" │                                      │")
    print(" └──────────────────────────────────────┘ \n")
    input("{}{} Press Enter to continue... {}".format(blink, cyan, reset))

# A primitive function to forcibly escape every RegEx-y character in variable.
def re_decoder(variable):
    variable = variable.replace("[", r"\[")
    variable = variable.replace("]", r"\]")
    variable = variable.replace(".", r"\.")
    variable = variable.replace("*", r"\*")
    variable = variable.replace("^", r"\^")
    variable = variable.replace("$", r"\$")
    variable = variable.replace("+", r"\+")
    variable = variable.replace("?", r"\?")
    variable = variable.replace("{", r"\{")
    variable = variable.replace("}", r"\}")
    variable = variable.replace("|", r"\|")
    variable = variable.replace("(", r"\(")
    variable = variable.replace(")", r"\)")
    variable = variable.replace("\A", r"\\A")
    variable = variable.replace("\b", r"\\b")
    variable = variable.replace("\B", r"\\B")
    variable = variable.replace("\d", r"\\d")
    variable = variable.replace("\D", r"\\D")
    variable = variable.replace("\s", r"\\s")
    variable = variable.replace("\S", r"\\S")
    variable = variable.replace("\w", r"\\w")
    variable = variable.replace("\W", r"\\W")
    variable = variable.replace("\Z", r"\\Z")
    return variable