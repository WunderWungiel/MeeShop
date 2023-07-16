import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import subprocess
from xml.etree import ElementTree as ET
import sys
sys.path.append("/opt/MeeShop/functions")

from clean import clean

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
    countries_files = []

    try:
        r = urlopen("http://wunderwungiel.pl/MeeGo/.database/.rss/countries.xml")
    except (URLError, HTTPError):
        print(" {}Error while downloading content!{}".format(red, reset))
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        return
    root_string = r.read().decode("utf-8")

    root = ET.fromstring(root_string)

    for i, country in enumerate(root.findall('country'), start=1):
        country_name = country.get('name')
        country_file = country.get('file')

        countries_numbers.append(str(i))
        countries_names.append(country_name)
        countries_files.append(country_file)
    

    while True:
        clean()
        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        print(" │           ╔═════════════╗            │")
        print(" │           ║  RSS feeds: ║            │")
        print(" │           ╚═════════════╝            │")
        print(" │                                      │")
        for i, name in zip(countries_numbers, countries_names):
                country = "{}. {}".format(i, name)
                lenght = " " * int((38 - 10 - len(country)))
                print(" │          {}{}│".format(country, lenght))
        print(" │                                      │")
        print(" │          0. Return                   │")
        print(" │                                      │")
        print(" └──────────────────────────────────────┘ \n")
        
        answer = input(" {}Select a country (digit):{} ".format(yellow, reset))
        if answer == "0":
            clean()
            return
        if answer not in countries_numbers:
            print(" {}Wrong number, select a correct one!{}".format(red, reset))
            time.sleep(2)
            continue
        else:
            pass

        country = countries_names[countries_numbers.index(answer)]
        country_file = countries_files[countries_numbers.index(answer)]

        while True:
            _ = country_feeds(country, country_file)
            if _ == "Break":
                break

def country_feeds(country, country_file):

    try:
        r = urlopen("http://wunderwungiel.pl/MeeGo/.database/.rss/{}".format(country_file))
    except (URLError, HTTPError):
        print(" {}Error while downloading content!{}".format(red, reset))
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        return "Break"
    
    root_string = r.read().decode("utf-8")
    root = ET.fromstring(root_string)

    while True:

        numbers = []
        names = []
        links = []

        for rss in root.findall('rss'):
            number = rss.get('num')
            name = rss.get('name')
            url = rss.get('url')

            numbers.append(number)
            names.append(name)
            links.append(url)

        clean()
        if len(country) % 2 != 0:
            country = " " + country
        lenght = " " * int((38 - 7 - len(country)) / 2)

        print(" ┌──────────────────────────────────────┐")
        print(" │                                      │")
        print(" │{}{} feeds:{}│".format(lenght, country, lenght))
        print(" │                                      │")
        for i, name in zip(numbers, names):
            feed = "{}. {}".format(i, name)
            lenght = " " * int((38 - 5 - len(feed)))
            print(" │     {}{}│".format(feed, lenght))
        print(" │                                      │")
        print(" │     0. Return                        │")
        print(" │                                      │")
        print(" └──────────────────────────────────────┘ \n")

        while True:
            selected = input(" {}Select a feed:{} ".format(yellow, reset))
            if selected == "0":
                clean()
                return "Break"
            if not selected.isnumeric() or selected not in numbers:
                print(" {}Wrong number, select a correct one!{}".format(red, reset))
                time.sleep(2)
                continue
            else:
                break

        link = links[numbers.index(selected)]

        subprocess.Popen("/usr/bin/invoker --type=m /usr/bin/grob {} > /dev/null 2>&1".format(link), shell=True)
        time.sleep(1.5)
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        continue