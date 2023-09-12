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

class Rss_Options:
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

class Country_Feeds_Options:
    def __init__(self):
        pass
    def feed(self, *args):

        links, numbers, i = args        

        link = links[numbers.index(i)]

        subprocess.Popen("/usr/bin/invoker --type=m /usr/bin/grob {} > /dev/null 2>&1".format(link), shell=True)
        time.sleep(1.5)
        tui.press_enter()()
    def exit(self):
        return "Break"

rss_list_options = Rss_Options()
country_feeds_options = Country_Feeds_Options()

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

        options = {}
        args = {}

        for i, name in zip(countries_numbers, countries_names):
                options[name] = rss_list_options.feed
                args[name] = [countries_names, countries_numbers, countries_files, i]
        options["Return"] = rss_list_options.exit

        while True:
            tui.clean()
            result = tui.menu(options=options, text=text, args=args)
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

        options = {}
        args = {}

        for i, name in zip(numbers, names):
            options[name] = country_feeds_options.feed
            args[name] = [links, numbers, i]

        options["Return"] = rss_list_options.exit

        while True:
            tui.clean()
            result = tui.menu(options=options, text=text, args=args)
            if result:
                return result