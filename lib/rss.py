import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import subprocess
from xml.etree import ElementTree as ET

from . import tui

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

class RSSOptions:
    def __init__(self):
        pass

    def feed(self, *args):

        countries_names, countries_numbers, countries_files, i = args

        country = countries_names[countries_numbers.index(i)]
        country_file = countries_files[countries_numbers.index(i)]

        while True:
            _ = country_feeds(country, country_file)
            if _ == "Break":
                break

    def exit(self):
        return "Break"

class CountryFeedsOptions:
    def __init__(self):
        pass

    def feed(self, *args):

        links, numbers, i = args        

        link = links[numbers.index(i)]

        subprocess.Popen(["/usr/bin/invoker", "--type=m", "/usr/bin/grob", link], stdout=subprocess.DEVNULL)
        time.sleep(1.5)
        tui.press_enter()()

    def exit(self):
        return "Break"

rss_list_options = RSSOptions()
country_feeds_options = CountryFeedsOptions()

def rss():

    countries_numbers = []
    countries_names = []
    countries_files = []

    try:
        r = urlopen("http://wunderwungiel.pl/MeeGo/.database/.rss/countries.xml")
    except (URLError, HTTPError):
        print(" {}Error while downloading content!{}".format(red, reset))
        tui.press_enter()()
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
        tui.clean()

        text = "RSS feeds:"

        items = []

        for i, name in zip(countries_numbers, countries_names):
                items.append([
                    name,
                    rss_list_options.feed,
                    [countries_names, countries_numbers, countries_files, i]
                ])
        items.append(["Return", rss_list_options.exit])

        while True:
            tui.clean()
            result = tui.menu(items, text=text)
            if result:
                return result

def country_feeds(country, country_file):

    try:
        r = urlopen("http://wunderwungiel.pl/MeeGo/.database/.rss/{}".format(country_file))
    except (URLError, HTTPError):
        print(" {}Error while downloading content!{}".format(red, reset))
        tui.press_enter()()
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

        tui.clean()

        text = "{} feeds:".format(country)

        items = []

        for i, name in zip(numbers, names):
            items.append([
                name,
                country_feeds_options.feed,
                [links, numbers, i]
            ])
        
        items.append(["Return", rss_list_options.exit])

        while True:
            tui.clean()
            result = tui.menu(items, text=text, space_left=3)
            if result:
                return result
