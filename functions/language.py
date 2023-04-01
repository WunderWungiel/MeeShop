import sys
from .clean import clean

def init(lang):
    global strings
    if lang == "en":
        from langs.en import Strings
    elif lang == "ru":
        from langs.ru import Strings

    strings = Strings()

def language():

    while True:
        clean()
        strings.change_language()
        language = strings.input_your_language()

        if language not in ["1", "2", "0"]:
            strings.wrong_number()
            strings.press_enter_to_continue()
            continue

        if language == "1":
            with open(".config", "w") as f:
                f.write("lang = en")
            print()
            strings.restart_app()
            strings.press_enter_to_continue()
            sys.exit(0)
        elif language == "2":
            with open(".config", "w") as f:
                f.write("lang = ru")
            print()
            strings.restart_app()
            strings.press_enter_to_continue()
            clean()
            sys.exit(0)
        else:
            return