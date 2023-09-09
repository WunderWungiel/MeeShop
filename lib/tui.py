"""`menu()` takes three arguments:

- `options`: a dictionary with following syntax:

`{'name': action, 'name2': action2}`

- `text` (optional) - a title to display
- `args` - optional args to pass to function with following syntax:

`{'name': ['arg1', 'arg2'], 'name2': ['arg1', 'arg2', 'arg3]}`

Before running menu() it's advised to run tui.clean() first.
"""
import subprocess
import sys
from time import sleep
import tty
import termios
import os

cyan = '\033[38;5;104m'
cyan_background = '\033[48;5;104m'
bold = '\033[1m'
italic = '\033[3m'
reset = '\033[0m'
blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'

def clean():
    subprocess.call("clear")

def rprint(text, time=0.02, previous_text='', _end="\n\n"):
    for s in text:

        s = "\r" + previous_text + s
        sys.stdout.write(s)

        previous_text = s
        sleep(time)
    print(_end, end='')

def get_arrow_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    while True:
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        
            if ch == '\x1b':
                ch = sys.stdin.read(2)
                if ch == '[A':
                    return "up"
                elif ch == '[B':
                    return "down"
                elif ch == '[F':
                    return "end"
                elif ch == '[H':
                    return "home"
            elif ch == "\x03":
                raise KeyboardInterrupt
            elif ch == "\r":
                return "enter"             
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_enter_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setraw(fd)
        sys.stdin.read(1)
        return "enter"              
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def menu(options, text=None, args=None, custom_text=None):

    options_names = list(options.keys())
    options_actions = list(options.values())
    options_integers = []

    for i, name in enumerate(options_names, start=1):
        options_integers.append(i)

    current_chosen = 1

    key = None

    first_iteration = True

    while True:

        """if not first_iteration:

            if text:
                to_clean = "\x1b[" + str(len(options_names) + 8) + "A"
            elif custom_text:
                lines_count = len(custom_text.splitlines())
                to_clean = "\x1b[" + str(len(options_names) + lines_count + 5) + "A"
            else:
                to_clean = "\x1b[" + str(len(options_names) + 5) + "A"

            sys.stdout.write(to_clean)
            sys.stdout.write("\x1b[0J")
            sys.stdout.flush()
            #clear_terminal_to_marker(" └──────────────────────────────────────┘")

        else:
            first_iteration = False""" #deprecated
        clean()

        
        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        
        if text:
            if len(text) % 2 != 0:
                text = " " + text

            spaces_count = (38 - len(text) - 6) // 2
            spaces = " " * spaces_count
            gora_count = 38 - (spaces_count * 2) - 2
            gora_spacje = "═" * gora_count
            gora_ramki = f" │{spaces}╔{gora_spacje}╗{spaces}│"
            print(gora_ramki)

            srodek_ramki = f" │{spaces}║  {text}  ║{spaces}│"
            print(srodek_ramki)

            gora_ramki = f" │{spaces}╚{gora_spacje}╝{spaces}│"
            print(gora_ramki)        

            print(" │                                      │")
        elif custom_text:
            print(custom_text)

        for i, name in zip(options_integers, options_names):

            if current_chosen < 1:
                current_chosen = options_integers[-1]
            elif current_chosen > options_integers[-1]:
                current_chosen = 1

            if current_chosen == i:

                if len(str(i)) % 2 == 0:
                    if len(name) % 2 != 0:
                        name += " "

                spaces = (27 - len(name) - len(str(i)))
                spaces = " " * spaces

                print(f" │         {cyan_background}{i}. {name}{reset}{spaces}│")
            else:

                if len(str(i)) % 2 == 0:
                    if len(name) % 2 != 0:
                        name += " "
                spaces = (27 - len(name) - len(str(i)))
                spaces = " " * spaces
                print(f" │         {i}. {name}{spaces}│")
        print(" │                                      │")
        print(" └──────────────────────────────────────┘")
        
        key = get_arrow_key()
        
        if key == "down":
            current_chosen += 1
        elif key == "up":
            current_chosen -= 1
        elif key == "enter":
            user_choose = current_chosen

            if args:
                user_choose_name = options_names[options_integers.index(user_choose)]
                if user_choose_name in args.keys():
                    args_list = list(args.get(user_choose_name))
                    result = options_actions[options_integers.index(user_choose)](*args_list)
                else:
                    result = options_actions[options_integers.index(user_choose)]()
            else:
                result = options_actions[options_integers.index(user_choose)]()
            if result:
                return result
        elif key == "end":
            current_chosen = options_integers[-1]
        elif key == "home":
            current_chosen = options_integers[0]