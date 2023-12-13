import sys
import termios
import tty
import time
from ..small_libs import quit
from ..tui import Menu

def save_terminal_state():
    fd = sys.stdin.fileno()
    original_settings = termios.tcgetattr(fd)
    return fd, original_settings

def set_terminal_to_raw(fd):
    tty.setraw(fd)

def clear_screen():
    sys.stdout.write("\033c")
    sys.stdout.flush()

def display_popup(message, duration):
    clear_screen()
    sys.stdout.write(message)
    sys.stdout.flush()
    time.sleep(duration)

def restore_terminal_state(fd, original_settings):
    termios.tcsetattr(fd, termios.TCSANOW, original_settings)

fd, original_settings = save_terminal_state()

try:
    items = [
        ['Opcja', display_popup, ["Yeah", 3]],
        '',
        ['Exit', quit]
    ]

    menu = Menu(items=items)

    while True:
        menu.show()

    # Tutaj wracasz do menu lub wykonujesz inne akcje.

finally:
    restore_terminal_state(fd, original_settings)