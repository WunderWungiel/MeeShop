import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import subprocess
from xml.etree import ElementTree as ET

from . import tui
from .tui import TUIMenu, Item
from .small_libs import press_enter

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def open_feed(link):

    subprocess.Popen(["/usr/bin/invoker", "--type=m", "/usr/bin/grob", link], stdout=subprocess.DEVNULL)
    time.sleep(1.5)
    press_enter()

def rss():

    countries_names = []
    countries_files = []

    try:
        r = urlopen("http://wunderwungiel.pl/MeeGo/.database/.rss/countries.xml")
    except (URLError, HTTPError):
        print(f" {red}Error while downloading content!{reset}")
        press_enter()
        return
    root_string = r.read().decode("utf-8")

    root = ET.fromstring(root_string)

    for country in root.findall('country'):
        country_name = country.get('name')
        country_file = country.get('file')

        countries_names.append(country_name)
        countries_files.append(country_file)
    
    menu = TUIMenu()
    menu.text = "RSS feeds:"

    for name, file in zip(countries_names, countries_files):
            menu.items.append(
                Item(
                    name,
                    country_feeds,
                    (name, file),
                    menu=True
                )
            )
    menu.items += ['', Item("Return", returns=True)]
    return menu

def country_feeds(country, country_file):

    try:
        r = urlopen(f"http://wunderwungiel.pl/MeeGo/.database/.rss/{country_file}")
    except (URLError, HTTPError):
        print(f" {red}Error while downloading content!{reset}")
        press_enter()
        return "break"
    
    root_string = r.read().decode("utf-8")
    root = ET.fromstring(root_string)

    names = []
    links = []

    for rss in root.findall('rss'):
        name = rss.get('name')
        url = rss.get('url')

        names.append(name)
        links.append(url)

    menu = TUIMenu(space_left=3)
    menu.text = f"{country} feeds:"
    
    for name, link in zip(names, links):
        menu.items.append(
            Item(
                name,
                open_feed,
                link
            )
        )
        
    menu.items += ['', Item("Return", returns=True)]

    return menu