import sys
import termios
import tty
import re

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

# Getting raw content of given string without any ANSI sentences.
def get_raw_string(string):
    # The right RegEx expression in use of re.sub.
    string = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', string)
    return string