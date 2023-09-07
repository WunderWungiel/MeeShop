import subprocess
import sys
from time import sleep
import tty
import termios

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
            elif ch == "\x03":
                sys.exit(0)
            elif ch == "\r":
                return "enter"
            elif ch == "\x1b[1;5F":
                return "end"               
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

def menu(text, options):

    options_names = list(options.keys())
    options_actions = list(options.values())
    options_integers = []

    for i, name in enumerate(options_names, start=1):
        options_integers.append(i)

    current_chosen = 1

    key = None

    first_iteration = True

    while True:

        if not first_iteration:

            to_clean = "\x1b[" + str(len(options_names) + 9) + "A"

            sys.stdout.write(to_clean)
            sys.stdout.write("\x1b[0J")
            sys.stdout.flush()

        first_iteration = False

        clean()

        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        
        if len(text) % 2 != 0:
            text += " "

        
       #print(" │       ╔═══════════════════════╗      │")

        spaces_count = (38 - len(text) - 6) // 2
        spaces = " " * spaces_count
        gora_count = 38 - (spaces_count * 2) - 2
        gora_spacje = "═" * gora_count
        gora_ramki = f" │{spaces}╔{gora_spacje}╗{spaces}│"
        print(gora_ramki)

        ###

        spaces_count = (38 - len(text) - 6) // 2
        spaces = " " * spaces_count
        spaces_inside_count = ((len(text)) - (spaces_count * 2) - 4) // 2
        spaces_inside = " " * spaces_inside_count

        print(f" │{spaces}║{spaces_inside}{text}{spaces_inside}║{spaces}│")

        ###

        spaces_count = (38 - len(text) - 6) // 2
        spaces = " " * spaces_count
        gora_count = 38 - (spaces_count * 2) - 2
        gora_spacje = "═" * gora_count
        gora_ramki = f" │{spaces}╚{gora_spacje}╝{spaces}│"
        print(gora_ramki)        

        print(" │                                      │")

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
            result = options_actions[options_integers.index(user_choose)]()
            if result:
                return result
            #get_enter_key()
            #sys.stdout.write("\x1b[1A")
            #sys.stdout.write("\x1b[0J")
            #sys.stdout.flush()
        elif key == "end":
            current_chosen = options_integers[-1]