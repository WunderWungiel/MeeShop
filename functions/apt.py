import subprocess
import sys
import os
import re
from urllib.request import urlopen
from urllib.parse import urljoin
import time
sys.path.append("functions")
from tqdm import tqdm
import dbc

db_creator = dbc.Db_creator()
ovi_db = db_creator.ovi_db
db = db_creator.db
full_db = db_creator.full_db
libs_db = db_creator.libs_db

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def meeshop_update():
    if check_update('meeshop'):
        answer = input(" Update available, wanna update now?")
        if answer.lower() in ["y", "yes"]:
            download("meeshop")
            install("meeshop")
        else:
            print(" Returning...")
            print()
            pass
    else:
        print(" No updates available!")
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

def download(package, prompt=True, mydocs=False):

    file = full_db[package]['file']

    link = urljoin("http://wunderwungiel.pl/MeeGo/openrepos/", file)
    print(" {}{}WAIT!{}{} Downloading...\n{}".format(red, blink, reset, red, reset))      
    response = urlopen(link)
    total_size_in_bytes = int(response.headers.get('Content-Length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    if mydocs:
        f = open(os.path.join("/home/user/MyDocs/", file), "wb")
    else:
        f = open(file, "wb")
    while True:
        data = response.read(block_size)
        if not data:
            break
        progress_bar.update(len(data))
        f.write(data)
        
    f.close()

    progress_bar.close()
    print()
    if prompt:
        if not mydocs:
            print(" Saved {} in /opt/MeeShop/.cache!\n".format(file))
        else:
            print(" Saved {} in /home/user/MyDocs!\n".format(file))

def ovi_download(file, link, prompt=True, mydocs=False):
    print(" {}{}WAIT!{}{} Downloading...\n{}".format(red, blink, reset, red, reset))       
    response = urlopen(link)
    total_size_in_bytes = int(response.headers.get('Content-Length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    if mydocs:
        f = open(os.path.join("/home/user/MyDocs/", file), "wb")
    else:
        f = open(file, "wb")
    while True:
        data = response.read(block_size)
        if not data:
            break
        progress_bar.update(len(data))
        f.write(data)
    f.close()
    progress_bar.close()
    print()
    if prompt:
        if not mydocs:
            print(" Saved {} in /opt/MeeShop/.cache!\n".format(file))
        else:
            print(" Saved {} in /home/user/MyDocs!\n".format(file))

def check_update(package):
    try:
        result = subprocess.check_output("LANG=C dpkg-query -s {}".format(package), shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        result = e.output
    result = result.decode("utf-8")
    version = re.search("Version: (.+)", result)
    if not version:
        return "Error"
    version = version.group(1)
    if version != full_db[package]['version']:
        return True
    else:
        return False

def is_installed(package):
    try:
        result = subprocess.check_output("LANG=C dpkg-query -s {}".format(package), shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        result = e.output
    result = result.decode("utf-8")
    if re.search("Status:.*ok installed.*", result):
        return True
    else:
        return False

def install(package):

    display_name = db[package]['display_name']
    filename = db[package]['file']

    print(" Installing...")
    print(" ")
    filepath = os.path.join("/opt/MeeShop/.cache", filename)
    command = 'LANG=C aegis-dpkg -i "{}"'.format(filepath)
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        result = result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        result = e.output
        result = result.decode("utf-8")
        depends = re.findall("depends on (.+);", result)
        if depends:
            depends = ', '.join(depends)
            print(" Package {} depends on following\n dependencies, not installed yet:\n\n {}.".format(display_name, depends))

            apt_depends = None

            for depend in depends:
                if not depend_install_meeshop:
                    apt_depends = True
                    continue
                install_depend(depend)

            if apt_depends:

                print(" Following dependencies were not found in MeeShop:")
                print(", ".join(apt_depends))
                print("Trying APT Fixer...")

                time.sleep(1)

                fix()

            print(" Completed! Check if everything works.")

        else:
            print(" Some error occured... Output:")
            print()
            print(" ########################################")
            print()
            print(result)
            print()
            print(" ########################################")
            print()

            input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

            return

    print(" ")
    print(" {}{} installed!{}".format(green, display_name, reset))
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

def ovi_install(display_name, filename):

    print(" Installing...")
    print(" ")
    filepath = os.path.join("/opt/MeeShop/.cache", filename)
    command = 'LANG=C aegis-dpkg -i "{}"'.format(filepath)
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        result = result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        result = e.output
        result = result.decode("utf-8")
        depends = re.findall("depends on (.+);", result)
        if depends:
            depends = ', '.join(depends)
            print(" Package {} depends on following\n dependencies, not installed yet:\n\n {}.".format(display_name, depends))

            apt_depends = None

            for depend in depends:
                if not depend_install_meeshop:
                    apt_depends = True
                    continue
                install_depend(depend)

            if apt_depends:

                print(" Following dependencies were not found in MeeShop:")
                print(", ".join(apt_depends))
                print("Trying APT Fixer...")

                time.sleep(1)

                fix()

            print(" Completed! Check if everything works.")

        else:
            print(" Some error occured... Output:")
            print()
            print(" ########################################")
            print()
            print(result)
            print()
            print(" ########################################")
            print()

            input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

            return

    print(" ")
    print(" {}{} installed!{}".format(green, display_name, reset))
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))


def uninstall(package):
    output = subprocess.call(
        "LANG=C dpkg -r {}".format(package),
        shell=True,
        stdout=open("/dev/null", "w")
    )
    if output != 0:
        print(" Something went wrong while uninstalling...\n Try uninstalling manually." )
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
    
def fix():
    subprocess.call("aegis-apt-get install -f", shell=True)
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

def install_depend(package):
    display_name = full_db[package]['display_name'] 
    filename = full_db[package]['file']

    download(package, prompt=True)
    install(package)

"""def depend_install_apt(package):
    result = subprocess.call("aegis-apt-get install -y {} > /dev/null 2>&1".format(package), shell=True)
    if result == 100:
        return False
    else:
        return True"""
    
def depend_install_meeshop(package):
    if package in full_db.keys():
        return True
    else:
        return False