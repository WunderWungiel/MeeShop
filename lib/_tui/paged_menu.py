from ..small_libs import clean, reset, isodd, iseven, remove_duplicates, split_item
from .term import get_key, get_raw_string, colors, bg_colors

class PagedMenu:
    def __init__(self, items=None, text=None, custom_text=None, width=38, items_on_page=10, space_left=9, repeat=False, text_color="default", highlight_color="cyan"):

        if not items:
            items = []

        self.text, self.custom_text = text, custom_text
        self.items, self.repeat = items, repeat
        self.width, self.items_on_page, self.space_left = width, items_on_page, space_left

        # The first selected item and first page are the firsts one.
        self.current_chosen = 0
        self.current_page = 0

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
        
        i = 0

        # Define four lists, containing:
        # - names
        # - actions to execute (should be object)
        # - integers (indexes)
        # - arguments to be passed to action (list with arguments)

        self.integers = []
        self.args = []

        # Let's make the real index of items properties.
        # We will retrieve:
        # - names of items
        # - actions to do in case of selecting items
        # - integer of each account, starting with 0
        # - optional arguments to actions.
        # If name of item is empty, or None, it will be replaced with a break between items.

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
        
        # Do pages split
        self.pages = self.split_by_pages()
        self.current_options_integers = self.pages[0]

        # Get the absolute index.
        if self.repeat:
            self.repeat = self.repeat if self.repeat > 0 else len(self.items) - abs(self.repeat)

        # Change commit flag to True
        self.commited = True

    def split_by_pages(self):
        
        # Create a pages dictionary. The example structure will be:
        # 
        # {
        #     0: [0, 1, 2, 3, 4],
        #     1: [5, 6, 7, 8, 9],
        #     2: [10]
        # }
        #

        pages = {}

        # If we use repeating, then lower items_on_page by 1
        items_on_page = self.items_on_page if not self.repeat else self.items_on_page - 1

        # Count number of full pages
        normal_parts_lenght = len(self.integers) // items_on_page
        # Retrieve indexes of items to be put on last page
        items_left = len(self.integers) - normal_parts_lenght * items_on_page
        
        start_index = 0
        
        for i in range(normal_parts_lenght):
            end_index = start_index + items_on_page
            pages[i] = self.integers[start_index:end_index]
            start_index += items_on_page

        pages[normal_parts_lenght] = self.integers[-items_left:]

        return pages

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
            lines.append(
                f"Page: {self.current_page+1} / {len(self.pages)}"
            )
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

                # Remove any ANSI sequences.
                raw_line = get_raw_string(line)

                if isodd(raw_line):
                    if list(raw_line)[0].isalpha():
                        line += " "
                    else:
                        line = " " + line

                spacje_w_srodku_count = (self.width - len(raw_line) - (spaces_count * 2) - 2) // 2
                spacje_w_srodku = " " * spacje_w_srodku_count

                middle_frame = f" │{spaces}║{spacje_w_srodku}{line}{spacje_w_srodku}║{spaces}│"
                print(middle_frame)

            gora_ramki = f" │{spaces}╚{gora_spacje}╝{spaces}│"
            print(gora_ramki)

            print(" │{}│".format(self.width * " "))
        # If it's custom text provided, just print it..
        elif self.custom_text:
            print(self.custom_text)
            print(f"\nPage: {self.current_page+1} / {len(self.pages)}")

        else:
            
            page_text = f"Page: {self.current_page+1} / {len(self.pages)}"
            spaces_count = (self.width - len(page_text) - 6) // 2
            spaces = " " * spaces_count
            gora_count = self.width - (spaces_count * 2) - 2
            gora_spacje = "═" * gora_count
            gora_ramki = f" │{spaces}╔{gora_spacje}╗{spaces}│"
            print(gora_ramki)
        
            if isodd(page_text):
                page_text += " "
            spacje_w_srodku_count = (self.width - len(page_text) - (spaces_count * 2) - 2) // 2
            spacje_w_srodku = " " * spacje_w_srodku_count

            srodek_ramki = f" │{spaces}║{spacje_w_srodku}{page_text}{spacje_w_srodku}║{spaces}│"
            print(srodek_ramki)

            gora_ramki = f" │{spaces}╚{gora_spacje}╝{spaces}│"
            print(gora_ramki)  
            print(" │{}│".format(self.width * " "))   

        # Finished printing title, now printing items names.

        self.current_options_integers = self.pages[self.current_page]
        # len(self.current_options_integers) is a nice way to get last index + 1
        if self.repeat and self.current_options_integers[-1] != self.repeat:
            self.current_options_integers.append(self.repeat)

        self.current_options_integers = remove_duplicates(self.current_options_integers)

        self.indexes = list(range(len(self.current_options_integers)))


        if self.current_chosen < self.current_options_integers[0]:
            self.current_chosen = self.current_options_integers[-1]
        elif self.current_chosen > self.current_options_integers[-1]:
            self.current_chosen = self.current_options_integers[0]

        being_on_repeated = False

        for index, i in zip(self.indexes, self.current_options_integers):

            # The visible page number should be greater by 1, so pages start with 1.
            # Internally it's still 0 and up, to make indexing easier.

            if self.repeat and self.current_options_integers[index] == self.repeat:
                being_on_repeated = True
            else:
                being_on_repeated = False

            visible_i = i+1 if not being_on_repeated else 0

            name = self.items[i].name

            available = self.width - 2 - self.space_left

            # In case of a blank line, just print correct amount of spaces,
            # and continue to next iteration.
            # if not name:
            #     spaces = self.width * " "
            #     print(f" │{spaces}│")
            #     continue

            if being_on_repeated:
                spaces = self.width * " "
                print(f" │{spaces}│")

            raw_name = get_raw_string(name)
            if iseven(len(str(visible_i))):
                if isodd(raw_name):
                    name += " "
            
            spaces_count = (available - len(raw_name) - len(str(visible_i)))
            spaces = " " * spaces_count

            # Retrieve parts of text (if it wouldn't fit in `width`)
            parts = split_item(name, i=visible_i, width=self.width, space_left=self.space_left)

            for part_index, part in enumerate(parts):

                if part_index == 0:
                    if self.current_chosen == i:
                        print(f" │         {self.highlight_color}{self.text_color}{visible_i}. {part[0]}{reset}{part[1] * ' '}  │")
                    else:
                        print(f" │         {self.text_color}{visible_i}. {part[0]}{part[1] * ' '}{reset}  │")
        
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
            if self.repeat:
                if self.current_chosen == self.current_options_integers[-2]:
                    self.current_chosen = self.current_options_integers[-1]
                elif self.current_chosen == self.current_options_integers[-1]:
                    self.current_chosen = self.current_options_integers[0]
                else:
                    self.current_chosen += 1
            else:
                self.current_chosen += 1
        elif key == "up":

            if self.repeat:
                if self.current_chosen == self.current_options_integers[-1]:
                    self.current_chosen = self.current_options_integers[-2]
                elif self.current_chosen == self.current_options_integers[0]:
                    self.current_chosen = self.current_options_integers[-1]
                else:
                    self.current_chosen -= 1
            else:
                self.current_chosen -= 1
        elif key == "right":
            self.current_page += 1
            if self.current_page < 0:
                self.current_page = len(self.pages) - 1
            elif self.current_page > len(self.pages) - 1:
                self.current_page = 0
            self.current_chosen = 0
        elif key == "left":
            self.current_page -= 1
            if self.current_page < 0:
                self.current_page = len(self.pages) - 1
            elif self.current_page > len(self.pages) - 1:
                self.current_page = 0
            self.current_chosen = 0
        elif key == "enter" or key == "space":
            item = self.items[self.integers.index(self.current_chosen)]

            if item.returns:
                return "break"

            args = self.args[self.integers.index(self.current_chosen)]
            action = item.action
            if not action:
                return

            if isinstance(action, (self.TUIMenu, self.Menu, PagedMenu, self.MultiSelectionMenu, self.MultiSelectionPagedMenu)):
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
            self.current_chosen = self.current_options_integers[-1]
        elif key == "home":
            self.current_chosen = self.current_options_integers[0]