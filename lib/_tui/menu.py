from ..small_libs import clean, reset, isodd, iseven, split_item
from .term import get_key, get_raw_string, colors, bg_colors
import time

class Menu:

    def __init__(self, items, text=None, custom_text=None, width=38, space_left=9, text_color="default", highlight_color="cyan"):
    
        if not items:
            items = []

        self.text, self.custom_text, self.items = text, custom_text, items
        self.width, self.space_left = width, space_left

        # The first selected item and first page are the firsts one.
        self.current_chosen = 0

        # Define a flag that will change to True, if user uses commit() (mandatory)
        self.commited = False

        if not text_color in colors.keys():
            raise Exception(f"Specified color doesn't exist.\n{colors.keys()}")
        if not highlight_color in bg_colors.keys():
            raise Exception(f"Specified color doesn't exist.\n{bg_colors.keys()}")
        self.text_color = colors[text_color]
        self.highlight_color = bg_colors[highlight_color]
        
        self.TUIMenu = None
        self.Menu = None
        self.PagedMenu = None
        self.MultiSelectionMenu = None
        self.MultiSelectionPagedMenu = None

    def commit(self):

        # Let's make the real index of items properties.
        # We will retrieve:
        # - names of items
        # - actions to do in case of selecting items
        # - optional arguments to actions.
        # If name of item is empty, or None, it will be replaced with a break between items.

        i = 0

        self.integers = []
        self.args = []

        for item in self.items:

            if not item:
                self.integers.append(None)
                self.args.append(())
                continue

            if item.args:
                # If it's one argument...
                if (
                    not isinstance(item.args, list) and
                    not isinstance(item.args, tuple) and
                    not isinstance(item.args, set)
                ):
                    self.args.append([item.args])
                # Else if it's list / tuple / set and has more than ONE argument...
                else:
                    self.args.append(item.args)
            else:
                self.args.append(())
            
            self.integers.append(i)
            i += 1
                
    def show(self):

        clean()
        
        print(" ┌{}┐".format(self.width * "─"))
        print(" │{}│".format(self.width * " "))
        
        #
        # Below is true if the text is selected to be proceeded automatically.
        # I.e. in case of text = "Welcome", we will get:
        # ╔═══════════╗
        # ║  Welcome  ║
        # ╚═══════════╝
        # With │ on left and right.
        #
        if self.text:
            # Split text into lines, and strip each line.
            lines = self.text.splitlines()
            lines = [line.strip() for line in lines]

            # Get biggest line, using length as key.
            biggest_line = max(lines, key=len)

            # Here is first bigger counting.
            # width = the available space between two │ characters.
            # len(get_raw_string(biggest_line)) = length of biggest line with removed ANSI sequences.
            # 6 = 2 free spaces on each side - 4, and two characters (╔ & ╗).
            # And we devide entire result with 2.
            spaces_count = (self.width - len(get_raw_string(biggest_line)) - 6) // 2
            spaces = " " * spaces_count
            gora_count = self.width - (spaces_count * 2) - 2
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

                spacje_w_srodku_count = (self.width - len(raw_line) - (spaces_count * 2) - 2) // 2
                spacje_w_srodku = " " * spacje_w_srodku_count

                srodek_ramki = f" │{spaces}║{spacje_w_srodku}{line}{spacje_w_srodku}║{spaces}│"
                print(srodek_ramki)

            gora_ramki = f" │{spaces}╚{gora_spacje}╝{spaces}│"
            print(gora_ramki)        

            print(" │{}│".format(self.width * " "))
        # If it's custom text provided, just print it.
        elif self.custom_text:
            print(self.custom_text)

        # Finished printing title, now printing items names.
        for i, item in zip(self.integers, self.items):

            if self.current_chosen < 0:
                self.current_chosen = self.integers[-1]
            elif self.current_chosen > self.integers[-1]:
                self.current_chosen = 0

            available = self.width - 2 - self.space_left

            if not item:
                spaces = self.width * " "
                print(f" │{spaces}│")
                continue

            visible_i = i+1

            raw_name = get_raw_string(item.name)
            if iseven(len(str(visible_i))):
                if isodd(raw_name):
                    item.name += " "
            spaces_count = (available - len(raw_name) - len(str(visible_i)))
            spaces = " " * spaces_count

            parts = split_item(item.name, i=visible_i, width=self.width, space_left=self.space_left)

            for part_index, part in enumerate(parts):

                if part_index == 0:
                    if self.current_chosen == i:
                        print(f" │{' ' * self.space_left}{self.highlight_color}{self.text_color}{visible_i}. {part[0]}{reset}{part[1] * ' '}  │")
                    else:
                        print(f" │{' ' * self.space_left}{self.text_color}{visible_i}. {part[0]}{part[1] * ' '}{reset}  │")

                elif part_index == (len(parts) - 1):
                    if self.current_chosen == i:
                        print(f" │  {self.highlight_color}{self.text_color}{part[0]}{reset}{part[1] * ' '}│")
                    else:
                        print(f" │  {self.text_color}{part[0]}{part[1] * ' '}{reset}│")
                else:
                    if self.current_chosen == i:
                        print(f" │  {self.highlight_color}{self.text_color}{part[0]}{reset}  │")
                    else:
                        print(f" │  {self.text_color}{part[0]}{reset}  │")


        print(" │{}│".format(self.width * " "))
        print(" └{}┘".format(self.width * "─"))

        key = get_key()

        if key == "down":
            self.current_chosen += 1
        elif key == "up":
            self.current_chosen -= 1
        elif key == "enter":

            item = self.items[self.integers.index(self.current_chosen)]

            if item.returns:
                return "break"

            args = self.args[self.integers.index(self.current_chosen)]
            action = item.action

            if not action:
                return

            if isinstance(action, (self.TUIMenu, Menu, self.PagedMenu, self.MultiSelectionMenu, self.MultiSelectionPagedMenu)):
                action.commit()
                while True:
                    result = action.show()
                    if result == "break":
                        break
            elif item.menu:

                if len(args) == 0:
                    menu = action()
                elif len(args) == 1:
                    menu = action(args[0])
                else:
                    menu = action(*args)

                menu.commit()
                while True:
                    result = menu.show()
                    if result == "break":
                        break

            elif len(args) == 0:
                result = action()
            elif len(args) == 1:
                result = action(args[0])
            else:
                result = action(*args)
            if result == "break":
                return
            elif result:
                return result
        
        elif key == "end":
            self.current_chosen = self.last_i
        elif key == "home":
            self.current_chosen = 0