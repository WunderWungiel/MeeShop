from urllib.request import urlopen
from xml.etree import ElementTree as ET

class Db_creator:

    def __init__(self):
        self.db = self.db_creator()
        self.ovi_db = self.ovi_db_creator()
        self.libs_db = self.lib_db_creator()

        self.full_db = {**self.db, **self.libs_db}

    def db_creator(self):
        r = urlopen("http://wunderwungiel.pl/MeeGo/openrepos/catalog_new.xml")
        with open("catalog.xml", "w") as f:
            f.write(r.read().decode("utf-8"))

        tree = ET.parse('catalog.xml')
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
    
    def lib_db_creator(self):
        r = urlopen("http://wunderwungiel.pl/MeeGo/openrepos/libs.xml")
        with open("catalog.xml", "w") as f:
            f.write(r.read().decode("utf-8"))

        tree = ET.parse('catalog.xml')
        root = tree.getroot()

        libs_db = {}

        for app in root.findall('app'):
            package = app.find('data').get('package')
            display_name = app.find('data').get('name')
            developer = app.find('data').get('dev')
            version = app.find('data').get('ver')
            file = app.find('data').get('deb')
            size = app.find('data').get('size')
    
            libs_db[package] = {
                'file': file,
                'version': version,
                'developer': developer,
                'package': package,
                'display_name': display_name,
                'size': size
            }
    
        return libs_db

    def ovi_db_creator(self):
        r = urlopen("http://wunderwungiel.pl/MeeGo/.database/Ovi.txt")
        with open("Ovi.txt", "w") as f:
            f.write(r.read().decode("utf-8"))
        with open("Ovi.txt", "r") as f:
            ovi_db = f.readlines()

        return ovi_db