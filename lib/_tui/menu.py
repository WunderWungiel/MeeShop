from ..small_libs import passer, clean, reset, cyan_background, isodd, iseven
from .term import get_key, get_raw_string

def split_item(text, width=38, space_left=9, i=1):
    i = str(i)
    i_length = len(i)
    text_length = len(text)

    parts = []

    #
    # First part
    #

    # Counting available space for first line.
    # width - space before i - 4 (two spaces * 2) - lenght of i

    first_available = width - space_left - 4 - i_length

    if text_length < first_available:
        left = first_available - text_length
        return [(text, left)]

    first_text = text[:first_available]
    first_text_length = len(first_text)

    first_left = first_available - first_text_length

    parts.append([first_text, first_left])

    _to_remove = text_length - first_available
    rest_of_text_all = text[-_to_remove:]

    #
    # Middle part
    #

    # Counting available space for second line.
    # width - 4 (two spaces * 2)
    middle_available = width - 4

    middle_parts = len(rest_of_text_all) // middle_available
    middle_text_length = (middle_parts * middle_available) + first_text_length

    start_index = first_text_length

    for part in range(middle_parts):
        
        end_index = start_index + middle_available
        part = text[start_index:end_index]
        start_index += middle_available

        parts.append([part, 0])

    #
    # Last part
    #

    last_index = text_length - middle_text_length
    last_text = text[-last_index:]
    last_text_length = len(last_text)
    last_left = width - 2 - last_text_length

    parts.append([last_text, last_left])

    return parts

def _menu(items, text=None, custom_text=None, width=38, space_left=9):

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
                    not isinstance(args, list) and
                    not isinstance(args, tuple) and
                    not isinstance(args, set)
                ):
                    options_args.append([args])
                # Elif it's list / tuple / set and has more than ONE argument...
                else:
                    options_args.append(args)
            else:
                options_args.append([])
            options_integers.append(i)
            i += 1

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

            print(" │{}│".format(width * " "))
        # If it's custom text provided, just print it, nothing else ;).
        elif custom_text:
            print(custom_text)

        # Finished printing title, now printing items names.
        for i, name in zip(options_integers, options_names):

            if current_chosen < 1:
                current_chosen = options_integers[-1]
            elif current_chosen > options_integers[-1]:
                current_chosen = 1

            available = width - 2 - space_left

            if not name:
                spaces = width * " "
                print(f" │{spaces}│")
                continue

            raw_name = get_raw_string(name)
            if iseven(len(str(i))):
                if isodd(raw_name):
                    name += " "
            spaces_count = (available - len(raw_name) - len(str(i)))
            spaces = " " * spaces_count

            # if current_chosen == i:
            #     print(f" │{space_left * ' '}{i}. {cyan_background}{name}{reset}{spaces}│")
            # else:
            #     print(f" │{space_left * ' '}{i}. {name}{spaces}│")
            parts = split_item(name, i=i)

            for part_index, part in enumerate(parts):

                if part_index == 0:
                    if current_chosen == i:
                        print(f" │         {cyan_background}{i}. {part[0]}{reset}{part[1] * ' '}  │")
                    else:
                        print(f" │         {i}. {part[0]}{part[1] * ' '}  │")
    
                elif part_index == (len(parts) - 1):
                    if current_chosen == i:
                        print(f" │  {cyan_background}{part[0]}{reset}{part[1] * ' '}│")
                    else:
                        print(f" │  {part[0]}{part[1] * ' '}│")
                else:
                    if current_chosen == i:
                        print(f" │  {cyan_background}{part[0]}{reset}  │")
                    else:
                        print(f" │  {part[0]}  │")


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
            args = options_args[options_integers.index(user_choose)]
            if len(args) == 0:
                result = options_actions[options_integers.index(user_choose)]()
            elif len(args) == 1:
                result = options_actions[options_integers.index(user_choose)](args[0])
            else:
                result = options_actions[options_integers.index(user_choose)](*args)
            if result:
                return result
        elif key == "end":
            current_chosen = options_integers[-1]
        elif key == "home":
            current_chosen = options_integers[0]