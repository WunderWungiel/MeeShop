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
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |              RSS feeds:              |")    
        print(" |                                      |")
        for i, name in zip(countries_numbers, countries_names):
                country = "{}. {}".format(i, name)
                lenght = " " * int((38 - 10 - len(country)))
                print(" |          {}{}|".format(country, lenght))
        print(" |                                      |")
        print(" |          0. Return                   |")
        print(" |                                      |")
        print("  -------------------------------------- \n")
        
        country = input(" {}Select a country (digit):{} ".format(yellow, reset))
        if country == "0":
            clean()
            return
        if country not in countries_numbers:
            print(" {}Wrong number!{}".format(red, reset))
            time.sleep(2)
            continue
        else:
            break

    while True:

        country_name = countries_names[countries_numbers.index(country)]

        with urlopen("http://wunderwungiel.pl/MeeGo/.database/.rss/{}.txt".format(country_name.lower())) as r:
            r = r.read().decode("utf-8")
            numbers = re.findall("(\d{1,2}) \|", r)
            names = re.findall("\| (.+) \|", r)
            links = re.findall("\| (http.+)", r)

        clean()
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |           Feeds for {}:          |".format(country_name))
        print(" |                                      |")
        for i, name in zip(numbers, names):
            feed = "{}. {}".format(i, name)
            lenght = " " * int((38 - 5 - len(feed)))
            print(" |     {}{}|".format(feed, lenght))
        print(" |                                      |")
        print(" |     0. Return                        |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

        while True:
            selected = input(" {}Select a feed:{} ".format(yellow, reset))
            if selected == "0":
                clean()
                return
            if not selected.isnumeric() or selected not in numbers:
                print(" {}Wrong number!{}".format(red, reset))
                time.sleep(2)
                continue
            else:
                break

        link = links[numbers.index(selected)]

        subprocess.Popen("/usr/bin/invoker --type=m /usr/bin/grob {} > /dev/null 2>&1".format(link), shell=True)
        time.sleep(1.5)
        input(" {}{}Press any key to continue... {}".format(blink, cyan, reset))
        continue