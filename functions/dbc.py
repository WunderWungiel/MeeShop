from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from xml.etree import ElementTree as ET
import sys

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

class Db_creator:

    def __init__(self):

        try:
            r = urlopen("http://wunderwungiel.pl/MeeGo/openrepos/categories.xml")
        except (URLError, HTTPError):
            print(" {}Error while downloading content!{}".format(red, reset))
            input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
            sys.exit(1)

        with open("categories.xml", "w") as f:
            f.write(r.read().decode("utf-8"))

        tree = ET.parse('categories.xml')
        root = tree.getroot()

        categories = {}

        for category in root.findall('category'):
            name = category.get('name')
            id = category.get('id')
            file = category.get('file')

            categories[id] = {
                "file": file
            }
            categories[id]["name"] = name

            categories[id]["db"] = self.db_creator(file)

        categories["full"] = {
            "name": "Everything"
        }
        categories["full"]["db"] = categories["apps"]["db"]

        for category in categories.keys():
            if category == "full" or category == "apps":
                continue
            categories["full"]["db"].update(categories[category]["db"])
            
        self.categories = categories
        self.ovi_db = self.ovi_db_creator()

    def db_creator(self, file):
        try:
            r = urlopen("http://wunderwungiel.pl/MeeGo/openrepos/{}".format(file))
        except (URLError, HTTPError):
            print(" {}Error while downloading content!{}".format(red, reset))
            input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
            sys.exit(1)
        with open(file, "w") as f:
            f.write(r.read().decode("utf-8"))

        tree = ET.parse(file)
        root = tree.getroot()

        db = {}

        for app in root.findall('app'):
            package = app.find('data').get('package')
            display_name = app.find('data').get('name')
            developer = app.find('data').get('dev')
            version = app.find('data').get('ver')
            file = app.find('data').get('deb')
            size = app.find('data').get('size')
    
            db[package] = {
                'file': file,
                'version': version,
                'developer': developer,
                'package': package,
                'display_name': display_name,
                'size': size
            }
    
        return db

    def ovi_db_creator(self):
        r = urlopen("http://wunderwungiel.pl/MeeGo/.database/Ovi.txt")
        with open("Ovi.txt", "w") as f:
            f.write(r.read().decode("utf-8"))
        with open("Ovi.txt", "r") as f:
            ovi_db = f.readlines()

        return ovi_db