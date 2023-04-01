from .clean import clean

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def init(lang):
    global strings
    if lang == "en":
        from langs.en import Strings
    elif lang == "ru":
        from langs.ru import Strings

    strings = Strings()

def about():

    clean()

    strings.about()
    strings.press_enter_to_continue()
    clean()