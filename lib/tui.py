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

def rprint(text='', time=0.02, previous_text='', _end="\n\n"):
    for s in text:

        s = "\r" + previous_text + s
        sys.stdout.write(s)

        previous_text = s
        sleep(time)
    print(_end, end='')

def rinput(text='', time=0.0235, previous_text='', _end=''):
    rprint(text=text, time=time, previous_text=previous_text, _end=_end)
    answer = input()
    if answer:
        return answer

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    while True:
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        
            if ch == '\x1b':
                ch2 = sys.stdin.read(2)
                if ch2 == "[A":
                    return "up"
                elif ch2 == '[B':
                    return "down"
                elif ch2 == '[F':
                    return "end"
                elif ch2 == '[H':
                    return "home"
            elif ch == "\x03":
                raise KeyboardInterrupt
            elif ch == "\r":
                return "enter"
            elif ch.isnumeric():
                return ch
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
            #clear_terminal_to_marker(" ╰──────────────────────────────────────╯")

        else:
            first_iteration = False""" # deprecated but keeping for info
        clean()

        
        print(" ╭──────────────────────────────────────╮")
        print(" │                                      │")
        
        if text:
            if len(text) % 2 != 0:
                if list(text)[0].isalpha():
                    text += " "
                else:
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
        print(" ╰──────────────────────────────────────╯")

        key = get_key()

        if key == "down":
            current_chosen += 1
        elif key == "up":
            current_chosen -= 1
        elif key.isnumeric() or key == "enter":
            if key == "enter":
                user_choose = current_chosen
            elif key.isnumeric():
                key = int(key)
                if key not in options_integers:
                    continue
                current_chosen = key
                user_choose = key
            if args:
                user_choose_name = options_names[options_integers.index(user_choose)]
                if user_choose_name in args.keys():
                    args_list = list(args.get(user_choose_name))
                    if isinstance(args_list, str):
                        result = options_actions[options_integers.index(user_choose)](args_list)
                    else:
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

def press_enter():
    rinput("{}{} Press Enter to continue... {}".format(blink, cyan, reset))