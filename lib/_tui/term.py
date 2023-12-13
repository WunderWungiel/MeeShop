import sys
import termios
import tty
import re
import keyboard

bg_colors = {
    "cyan": '\033[48;5;104m',
    'pink': '\033[48;5;169m'
}

colors = {
    'default': '',
    'bold': '\033[96m',
    'red': '\033[31m',
    'green': '\033[32m',
    'blink': '\033[5m',
    'yellow': '\033[33m',
    'cyan': '\033[1;36m'
}

reset = '\033[0m'

# def get_key():
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
    
#     while True:
#         try:
#             tty.setraw(fd)
#             ch = sys.stdin.read(1)
        
#             if ch == '\x1b':
#                 ch2 = sys.stdin.read(2)
#                 if ch2 == "[A":
#                     return "up"
#                 elif ch2 == '[B':
#                     return "down"
#                 elif ch2 == '[D':
#                     return "left"
#                 elif ch2 == '[C':
#                     return "right"
#                 elif ch2 == '[F':
#                     return "end"
#                 elif ch2 == '[H':
#                     return "home"
#             elif ch == "\x03":
#                 raise KeyboardInterrupt
#             elif ch == "\r":
#                 return "enter"
#             elif ch == " ":
#                 return "space"
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_key():
    while True:
        try:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_UP:
                if event.name == "up":
                    return "up"
                elif event.name == "down":
                    return "down"
                elif event.name == "left":
                    return "left"
                elif event.name == "right":
                    return "right"
                elif event.name == "end":
                    return "end"
                elif event.name == "home":
                    return "home"
            elif event.event_type == keyboard.KEY_DOWN:
                if event.name == "space":
                    return "space"
                elif event.name == "enter":
                    return "enter"
        except KeyboardInterrupt:
            raise

# Getting raw content of given string without any ANSI sentences.
def get_raw_string(string):
    # The right RegEx expression in use of re.sub.
    string = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', string)
    return string