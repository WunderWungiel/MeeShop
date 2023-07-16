from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from xml.etree import ElementTree as ET
import os
import hashlib

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def md5sum(file_path):
    with open(file_path, 'rb') as file:
        md5_hash = hashlib.md5()
        while True:
            data = file.read(4096)
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.hexdigest()

class Db_creator:

    def __init__(self):

        self.error = None

        try:
            r = urlopen("http://wunderwungiel.pl/MeeGo/openrepos/categories.xml")
        except (URLError, HTTPError):
            print(" {}Error downloading categories list...\n{}".format(red, reset))
            self.error = True
            return

        categories = r.read().decode("utf-8")

        root = ET.fromstring(categories)

        categories = {}

        for category in root.findall('category'):
            name = category.get('name')
            id = category.get('id')
            file = category.get('file')

            md5_file = "{}.sum".format(id)

            categories[id] = {
                "file": file
            }

            if os.path.isfile(file):
                try:
                    r = urlopen("http://wunderwungiel.pl/MeeGo/openrepos/md5/{}".format(md5_file))
                except (URLError, HTTPError):
                    print(" {}Error downloading MD5 sums...\n{}".format(red, reset))
                    self.error = True
                    return

                server_md5 = r.read().decode("utf-8")
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
        categories["full"]["db"] = categories["apps"]["db"]

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
                r = urlopen("http://wunderwungiel.pl/MeeGo/openrepos/{}".format(file))
            except (URLError, HTTPError):
                print(" {}Error downloading {}...\n{}".format(red, file, reset))
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
        try:
            r = urlopen("http://wunderwungiel.pl/MeeGo/.database/Ovi.txt")
        except (HTTPError, URLError):
            print(" {}Error downloading Ovi database...\n{}".format(red, reset))
            self.error = True
            return
        with open("Ovi.txt", "w") as f:
            f.write(r.read().decode("utf-8"))
        with open("Ovi.txt", "r") as f:
            ovi_db = f.readlines()

        return ovi_db