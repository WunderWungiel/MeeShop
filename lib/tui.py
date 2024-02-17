import sys
from time import sleep
import re

from ._tui import get_raw_string
from ._tui.menu import Menu
from ._tui.paged_menu import PagedMenu
from ._tui.multiselection_menu import MultiSelectionMenu
from ._tui.multiselection_paged_menu import MultiSelectionPagedMenu
from .small_libs import clean, isodd, split_item

# Defining some colors.
cyan = '\033[38;5;104m'
cyan_background = '\033[48;5;104m'
bold = '\033[1m'
italic = '\033[3m'
reset = '\033[0m'
blue = '\033[96m'
red = '\033[31m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'

# A function which will return a multi-line string, containing text with frame around.
def frame_around_text(text, width=38):
    # This creates list from string and stips each line, to ensure there are not any whitespaces.
    lines = text.splitlines()
    lines = [line.strip() for line in lines]

    # We take biggest line by its lenght.
    biggest_line = max(lines, key=len)

    # Counting the spaces number on left and right.
    # First, we do a mathematical operation:
    # (width - raw content lenght of biggest line - 6), and we divide the result by 2
    # width means the available space between │ and │
    # 6 is the space inside and with double frame around text (║__text__║), where _ is space.
    spaces_count = (width - len(get_raw_string(biggest_line)) - 6) // 2
    spaces = " " * spaces_count
    # This counts number of top of frame, i.e. ═ characters.
    # width - total spaces count - 2
    # 2 means ╔ + ╗ here.
    top_count = width - (spaces_count * 2) - 2
    top_spaces = "═" * top_count
    top_frame = f" │{spaces}╔{top_spaces}╗{spaces}│"
    output = top_frame

    for line in lines:

        raw_line = get_raw_string(line)

        if isodd(raw_line):
            if list(raw_line)[0].isalpha():
                line += " "
            else:
                line = " " + line

        spaces_inside_count = (width - len(raw_line) - (spaces_count * 2) - 2) // 2
        spaces_inside = " " * spaces_inside_count

        middle_frame = f" │{spaces}║{spaces_inside}{line}{spaces_inside}║{spaces}│"
        output += "\n" + middle_frame

    bottom_frame = f" │{spaces}╚{top_spaces}╝{spaces}│"
    output += "\n" + bottom_frame
    
    return output 

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

class Item:
    def __init__(self, name="", action=None, args=[], returns=False, menu=False):
        self.name = name
        self.action = action
        self.args = args
        self.returns = returns
        self.menu = menu

class TUIMenu:
    def __init__(
        self,
        items=None,
        text=None,
        custom_text=None,
        width=38,
        space_left=9,
        text_color="default",
        highlight_color="cyan",
        paged=False,
        multiselection=False,
        items_on_page=10,
        repeat=-1
    ):
               
        if not items:
            items = []
        
        self.items, self.text, self.custom_text = items, text, custom_text
        self.space_left, self.width, self.repeat = space_left, width, repeat
        self.text_color, self.highlight_color = text_color, highlight_color
        self.paged, self.multiselection, self.items_on_page = paged, multiselection, items_on_page

    def commit(self):
        
        if self.paged:
            
            if self.multiselection:

                self.menu = MultiSelectionPagedMenu(
                    self.items, 
                    text=self.text,
                    custom_text=self.custom_text,
                    width=self.width,
                    space_left=self.space_left,
                    text_color=self.text_color,
                    highlight_color=self.highlight_color
                )

            else:

                self.menu = PagedMenu(
                    self.items,
                    text=self.text,
                    custom_text=self.custom_text,
                    width=self.width,
                    items_on_page=self.items_on_page,
                    space_left=self.space_left,
                    repeat=self.repeat,
                    text_color=self.text_color,
                    highlight_color=self.highlight_color
                )
        else:

            if self.multiselection:
                
                self.menu = MultiSelectionMenu(
                    self.items,
                    text=self.text,
                    custom_text=self.custom_text,
                    width=self.width,
                    space_left=self.space_left,
                    text_color=self.text_color,
                    highlight_color=self.highlight_color
                )

            else:

                self.menu = Menu(
                    self.items,
                    text=self.text,
                    custom_text=self.custom_text,
                    width=self.width,
                    space_left=self.space_left,
                    text_color=self.text_color,
                    highlight_color=self.highlight_color
                )

        self.menu.TUIMenu = TUIMenu
        self.menu.Menu = Menu
        self.menu.PagedMenu = PagedMenu
        self.menu.MultiSelectionMenu = MultiSelectionMenu
        self.menu.MultiSelectionPagedMenu = MultiSelectionPagedMenu

        self.menu.commit()

    def show(self):
        result = self.menu.show()
        if result or result == []:
            return result

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

                if isodd(raw_line):
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

                if isodd(raw_line):
                    if list(raw_line)[0].isalpha():
                        line += " "
                    else:
                        line = " " + line
                print(f" │{spaces}{line}{spaces}│")

        print(" │{}│".format(width * " "))
        print(" └{}┘ {}".format(width * "─", end))
    elif custom_text:
        print(custom_text)

def blank_line(width=38):
    return " │{}│".format(width * " ")