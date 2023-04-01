import time
from urllib.request import urlopen
import subprocess
import re

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

def rss():

    countries_numbers = []
    countries_names = []

    with urlopen("http://wunderwungiel.pl/MeeGo/.database/.rss/countries.txt") as r:
        r = r.read().decode("utf-8").splitlines()
        for i, line in enumerate(r, start=1):
            countries_numbers.append(str(i))
            countries_names.append(line)
    
    while True:
        clean()
        strings.rss_feeds()
        for i, name in zip(countries_numbers, countries_names):
                country = "{}. {}".format(i, name)
                lenght = " " * int((38 - 10 - len(country)))
                print(" |          {}{}|".format(country, lenght))
        strings.rss_feeds_return()
        
        country = strings.select_a_country_digit()
        if country == "0":
            clean()
            return
        if country not in countries_numbers:
            strings.wrong_number()
            time.sleep(2)
            continue
        else:
            pass

        while True:
            _ = country_feeds(country=country, countries_names=countries_names, countries_numbers=countries_numbers)
            if _ == "Break":
                break

def country_feeds(country, countries_names, countries_numbers):

    while True:

        country_name = countries_names[countries_numbers.index(country)]

        with urlopen("http://wunderwungiel.pl/MeeGo/.database/.rss/{}.txt".format(country_name.lower())) as r:
            r = r.read().decode("utf-8")
            numbers = re.findall("(\d{1,2}) \|", r)
            names = re.findall("\| (.+) \|", r)
            links = re.findall("\| (http.+)", r)

        clean()
        strings.feeds_for(country_name)
        for i, name in zip(numbers, names):
            feed = "{}. {}".format(i, name)
            lenght = " " * int((38 - 5 - len(feed)))
            print(" |     {}{}|".format(feed, lenght))
        strings.feeds_for_return()

        while True:
            selected = strings.select_a_feed()
            if selected == "0":
                clean()
                return "Break"
            if not selected.isnumeric() or selected not in numbers:
                strings.wrong_number()
                time.sleep(2)
                continue
            else:
                break

        link = links[numbers.index(selected)]

        subprocess.Popen("/usr/bin/invoker --type=m /usr/bin/grob {} > /dev/null 2>&1".format(link), shell=True)
        time.sleep(1.5)
        strings.press_enter_to_continue()
        continue