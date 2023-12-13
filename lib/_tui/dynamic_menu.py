from ..small_libs import quit, passer, isodd, iseven, clean, cyan_background, reset
from .term import get_key, get_raw_string
from .menu import split_item
from icecream import ic
class DynamicMenu:
    def __init__(self, items, text=None, custom_text=None, width=38, space_left=9, to_display=10):   
        self.options_integers, self.options_names, self.options_actions, self.options_args = self.get_options(items)
        self.text, self.custom_text, self.width, self.space_left, self.to_display = text, custom_text, width, space_left, to_display
        self.buffored = [0, 9]

    def run(self):
        self.print_items()

    def get_options(self, items):
        options_names = []
        options_actions = []
        options_integers = []
        options_args = []

        i = 1

        # Let's make the real index of items properties.
        # We will retrieve:
        # - names of items
        # - actions to do in case of selecting items
        # - integer of each account, starting with 0
        # - optional arguments to actions.
        # If name of item is empty, or None, it will be replaced with a break between items.
        for name in items:
            if not name:
                options_names.append('')
                options_actions.append(passer)
                options_integers.append(None)
                options_args.append([])
                # In this case we omit adding 1 to i, because this is just a break between items.
                continue
            else:
                options_names.append(name[0])
                options_actions.append(name[1])
                # If there are arguments...
                if len(name) > 2:
                    args = name[2]
                    # If it's one argument...
                    if (
                        not isinstance(args, (list, tuple, set))
                    ):
                        options_args.append([args])
                    # Elif it's list / tuple / set and has more than ONE argument...
                    else:
                        options_args.append(args)
                else:
                    options_args.append([])
                options_integers.append(i)
                i += 1
            
        return options_integers, options_names, options_actions, options_args

    def print_items(self):

        text, custom_text, width, space_left, to_display = self.text, self.custom_text, self.width, self.space_left, self.to_display
        options_integers, options_names, options_actions, options_args = self.options_integers, self.options_names, self.options_actions, self.options_args

        # The first selected item is first one.
        current_chosen = 1

        while True:

            clean()
            
            print(" ┌{}┐".format(width * "─"))
            print(" │{}│".format(width * " "))
            
            #
            # Below is true if the text is selected to be proceeded automatically.
            # I.e. in case of text = "Welcome", we will get:
            # ╔═══════════╗
            # ║  Welcome  ║
            # ╚═══════════╝
            # With │ on left and right.
            #
            if text:
                # Split text into lines, and strip each line.
                lines = text.splitlines()
                lines = [line.strip() for line in lines]

                # Get biggest line, using length as key.
                biggest_line = max(lines, key=len)

                # Here is first bigger counting.
                # width = the available space between two │ characters.
                # len(get_raw_string(biggest_line)) = length of biggest line with removed ANSI sequences.
                # 6 = 2 free spaces on each side - 4, and two characters (╔ & ╗).
                # And we devide entire result with 2.
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
            # If it's custom text provided, just print it, nothing else ;).
            elif custom_text:
                print(custom_text)

            # Counting the items names to print in each sequence

            normal_items = []
            last_items = []
            total_items_count = len(options_integers)
            normal_items_sequences_count = total_items_count // to_display
            last_items_count = total_items_count % to_display
            start = 0
            for i in range(normal_items_sequences_count):
                end_index = start + to_display
                normal_items.append([])
                normal_items[i] += options_names[start:end_index]
                start += to_display
            last_items = options_names[-last_items_count:]

            if not normal_items_sequences_count:
                self.buffored = [0, len(options_integers) - 1]
            else:
                self.buffored = [0, self.buffored[1] + to_display]
            ic(self.buffored)
            quit()

            # Finished printing title, now printing items names.
            first = 0
            #         if current_chosen < 1:
            #             current_chosen = options_integers[-1]
            #         elif current_chosen > options_integers[-1]:
            #             current_chosen = 1

            #         available = width - 2 - space_left

            #         if not name:
            #             spaces = width * " "
            #             print(f" │{spaces}│")
            #             continue

            #         raw_name = get_raw_string(name)
            #         if iseven(len(str(i))):
            #             if isodd(raw_name):
            #                 name += " "
            #         spaces_count = (available - len(raw_name) - len(str(i)))
            #         spaces = " " * spaces_count

            #         parts = split_item(name, i=i)

            #         for part_index, part in enumerate(parts):

            #             if part_index == 0:
            #                 if current_chosen == i:
            #                     print(f" │         {cyan_background}{i}. {part[0]}{reset}{part[1] * ' '}  │")
            #                 else:
            #                     print(f" │         {i}. {part[0]}{part[1] * ' '}  │")
            
            #             elif part_index == (len(parts) - 1):
            #                 if current_chosen == i:
            #                     print(f" │  {cyan_background}{part[0]}{reset}{part[1] * ' '}│")
            #                 else:
            #                     print(f" │  {part[0]}{part[1] * ' '}│")
            #             else:
            #                 if current_chosen == i:
            #                     print(f" │  {cyan_background}{part[0]}{reset}  │")
            #                 else:
            #                     print(f" │  {part[0]}  │")


            # # print(" │{}│".format(width * " "))
            # # print(" └{}┘".format(width * "─"))

            #     key = get_key()

            #     if key == "down":
            #         current_chosen += 1
            #     elif key == "up":
            #         current_chosen -= 1
            #     elif key.isnumeric() or key == "enter":
            #         if key == "enter":
            #             user_choose = current_chosen
            #         elif key.isnumeric():
            #             key = int(key)
            #             if key not in options_integers:
            #                 continue
            #             current_chosen = key
            #             user_choose = key
            #         args = options_args[options_integers.index(user_choose)]
            #         if len(args) == 0:
            #             result = options_actions[options_integers.index(user_choose)]()
            #         elif len(args) == 1:
            #             result = options_actions[options_integers.index(user_choose)](args[0])
            #         else:
            #             result = options_actions[options_integers.index(user_choose)](*args)
            #         if result:
            #             return result
            #     elif key == "end":
            #         current_chosen = options_integers[-1]
            #     elif key == "home":
            #         current_chosen = options_integers[0]