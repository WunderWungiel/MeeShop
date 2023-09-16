import subprocess
import sys
from time import sleep
import tty
import termios
import re

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
    
    if re.search(r'\x1B\[[0-?]*[ -/]*[@-~]', text):
        ansi_pattern = r'\x1B\[[0-?]*[ -/]*[@-~]'
        ansi_sequences = re.split(ansi_pattern, text)
        ansi_matches = re.findall(ansi_pattern, text)

        for text_part, ansi_seq in zip(ansi_sequences, ansi_matches):
            for char in text_part:
                sys.stdout.write(char)
                sys.stdout.flush()
                sleep(time)

            sys.stdout.write(ansi_seq)
            sys.stdout.flush()

        print(_end, end='')
    else:
        for s in text:

            s = "\r" + previous_text + s
            sys.stdout.write(s)
            sys.stdout.flush()

            previous_text = s
            sleep(time)
        print(_end, end='')

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

def get_raw_string(string):
    string = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', string)
    return string

def menu(options, text=None, args=None, custom_text=None, width=38, space_left=9):

    options_names = list(options.keys())
    options_actions = list(options.values())
    options_integers = []

    for i, name in enumerate(options_names, start=1):
        options_integers.append(i)

    current_chosen = 1

    key = None

    while True:

        clean()
        
        print(" ┌{}┐".format(width * "─"))
        print(" │{}│".format(width* " "))
        
        if text:
            lines = text.splitlines()
            lines = [line.strip() for line in lines]

            biggest_line = max(lines, key=len)

            spaces_count = (width - len(get_raw_string(biggest_line)) - 6) // 2
            spaces = " " * spaces_count
            gora_count = width - (spaces_count * 2) - 2
            gora_spacje = "═" * gora_count
            gora_ramki = f" │{spaces}╔{gora_spacje}╗{spaces}│"
            print(gora_ramki)

            for line in lines:

                raw_line = get_raw_string(line)

                if len(raw_line) % 2 != 0:
                    if list(raw_line)[0].isalpha():
                        line += " "
                    else:
                        line = " " + line

                spacje_w_srodku_count = (width - len(raw_line) - (spaces_count * 2) - 2) // 2
                spacje_w_srodku = " " * spacje_w_srodku_count

                srodek_ramki = f" │{spaces}║{spacje_w_srodku}{line}{spacje_w_srodku}║{spaces}│"
                print(srodek_ramki)

            gora_ramki = f" │{spaces}╚{gora_spacje}╝{spaces}│"
            print(gora_ramki)        

            print(" │{}│".format(width * " "))
        elif custom_text:
            print(custom_text)

        for i, name in zip(options_integers, options_names):

            if current_chosen < 1:
                current_chosen = options_integers[-1]
            elif current_chosen > options_integers[-1]:
                current_chosen = 1

            available = width - 2 - space_left

            if current_chosen == i:

                raw_name = get_raw_string(name)

                if len(str(i)) % 2 == 0:
                    if len(raw_name) % 2 != 0:
                        name += " "

                spaces = (available - len(raw_name) - len(str(i)))
                spaces = " " * spaces

                print(f" │{space_left * ' '}{cyan_background}{i}. {name}{reset}{spaces}│")
            else:

                raw_name = get_raw_string(name)

                if len(str(i)) % 2 == 0:
                    if len(raw_name) % 2 != 0:
                        name += " "
                spaces = (available - len(raw_name) - len(str(i)))
                spaces = " " * spaces
                print(f" │{space_left * ' '}{i}. {name}{spaces}│")
        print(" │{}│".format(width * " "))
        print(" └{}┘".format(width * "─"))

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
                    args_list = args.get(user_choose_name)
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

def frame(text=None, custom_text=None, width=38, end='\n', second_frame=False, clean_screen=True):
    if clean_screen:
        clean()
        
    print(" ┌{}┐".format(width * "─"))
    print(" │{}│".format(width* " "))

    if text:
        lines = text.splitlines()
        lines = [line.strip() for line in lines]
        raw_lines = [get_raw_string(line) for line in lines]
        biggest_line = max(raw_lines, key=len)
        if len(biggest_line) > 36:
            biggest_line = "".join(list(biggest_line)[:36])

        if second_frame:
        
            spaces_count = (width - len(biggest_line) - 6) // 2
            spaces = " " * spaces_count
            gora_count = width - (spaces_count * 2) - 2
            gora_spacje = "═" * gora_count
            gora_ramki = f" │{spaces}╔{gora_spacje}╗{spaces}│"
            print(gora_ramki)

            for line in lines:

                raw_line = get_raw_string(line)

                if len(raw_line) % 2 != 0:
                    if list(raw_line)[0].isalpha():
                        line += " "
                    else:
                        line = " " + line

                spacje_w_srodku_count = (width - len(raw_line) - (spaces_count * 2) - 2) // 2
                spacje_w_srodku = " " * spacje_w_srodku_count

                srodek_ramki = f" │{spaces}║{spacje_w_srodku}{line}{spacje_w_srodku}║{spaces}│"
                print(srodek_ramki)

            gora_ramki = f" │{spaces}╚{gora_spacje}╝{spaces}│"
            print(gora_ramki)           

        else:
            for line in lines:

                spaces_count = (width - len(get_raw_string(line))) // 2
                spaces = " " * spaces_count

                raw_line = get_raw_string(line)

                if len(raw_line) % 2 != 0:
                    if list(raw_line)[0].isalpha():
                        line += " "
                    else:
                        line = " " + line
                print(f" │{spaces}{line}{spaces}│")

        print(" │{}│".format(width * " "))
        print(" └{}┘ {}".format(width * "─", end))
    elif custom_text:
        print(custom_text)

def press_enter():
    input("{}{} Press Enter to continue... {}".format(blink, cyan, reset))