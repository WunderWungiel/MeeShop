from xml.etree import ElementTree as ET
import os
import hashlib
from copy import deepcopy

import requests

from .small_libs import reset, red, quit

def md5sum(file_path):
    with open(file_path, 'rb') as file:
        md5_hash = hashlib.md5()
        while True:
            data = file.read(4096)
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.hexdigest()

class DbCreator:

    def __init__(self):

        self.error = None

        try:
            r = requests.get("http://wunderwungiel.pl/MeeGo/openrepos/categories.xml")
        except requests.exceptions.RequestException as e:
            print(f" {red}Error downloading categories list... Error: {e}\n{reset}")
            self.error = True
            return

        categories = r.text

        root = ET.fromstring(categories)

        categories = {}

        for category in root.findall('category'):
            name = category.get('name')
            id = category.get('id')
            file = category.get('file')

            md5_file = f"{id}.sum"

            categories[id] = {
                "file": file
            }

            if os.path.isfile(file):
                try:
                    r = requests.get(f"http://wunderwungiel.pl/MeeGo/openrepos/md5/{md5_file}")
                except requests.exceptions.RequestException as e:
                    print(f" {red}Error downloading MD5 sums... Error: {e}\n{reset}")
                    self.error = True
                    return

                server_md5 = r.text
                server_md5 = server_md5.split("\n")[0]
                local_md5 = md5sum(file)

                if server_md5 == local_md5:
                    categories[id]["db"] = self.db_creator(file, download=False)
                else:
                    categories[id]["db"] = self.db_creator(file, download=True)
            else:
                categories[id]["db"] = self.db_creator(file, download=True)

            if self.error:
                return
            
            categories[id]["name"] = name

        categories["full"] = {
            "name": "Everything"
        }
        categories["full"]["db"] = deepcopy(categories["apps"]["db"])

        for category in categories.keys():
            if category == "full" or category == "apps":
                continue
            categories["full"]["db"].update(categories[category]["db"])

        self.categories = categories
        self.ovi_db = self.ovi_db_creator()
        if self.error:
            return

    def db_creator(self, file, download):
        
        if download:
            try:
                r = requests.get(f"http://wunderwungiel.pl/MeeGo/openrepos/{file}")
            except requests.exceptions.RequestException as e:
                print(f" {red}Error downloading {file}... Error: {e}\n{reset}")
                self.error = True
                return
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
            icon = app.find('data').get('icon')
    
            db[package] = {
                'file': file,
                'version': version,
                'developer': developer,
                'package': package,
                'display_name': display_name,
                'size': size,
                'icon': icon
            }
    
        return db

    def ovi_db_creator(self):
        try:
            r = requests.get("http://wunderwungiel.pl/MeeGo/.database/Ovi.txt")
        except requests.exceptions.RequestException as e:
            print(f" {red}Error downloading Ovi database... Error: {e}\n{reset}")
            self.error = True
            return
        with open("Ovi.txt", "w") as f:
            f.write(r.text)
        with open("Ovi.txt", "r") as f:
            ovi_db = f.readlines()

        return ovi_db

db_creator = DbCreator()
if db_creator.error:
    quit(1)

ovi_db = db_creator.ovi_db
categories = db_creator.categories