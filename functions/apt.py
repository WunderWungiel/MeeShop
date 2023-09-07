import subprocess
import sys
import os
import re
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError, URLError
import shutil
from tqdm import tqdm
from . import dbc

db_creator = dbc.Db_creator()
ovi_db = db_creator.ovi_db
categories = db_creator.categories
full_db = categories["full"]["db"]

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def update():
    result = subprocess.call("aegis-apt-get update", shell=True, stdout=open("/dev/null", "wb"), stderr=open("/dev/null", "wb"))
    if result != 0:
        return "Error"
    
def is_dpkg_locked():
    
    paths = [
        "/var/lib/dpkg/lock",
        "/var/lib/apt/lists/lock"
    ]

    for path in paths:


        if not os.path.isfile(path):
            continue

        try:
            result = subprocess.check_output("lsof {}".format(path), shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            result = e.output

        result = result.decode("utf-8")

        if "dpkg.real" in result or "apt-get.real" in result:
            return True
    
    return False

def meeshop_update():
    if check_update('meeshop'):
        answer = input(" {}Update available, wanna update now?{} ".format(cyan, reset))
        if answer.lower() in ["y", "yes"]:
            try:
                install("meeshop")
            except Exception as e:
                print(" Error {}{}{}! Report to developer.".format(red, e, reset))
                input(" {}{}Press Enter to exit... {}".format(blink, cyan, reset))
                sys.exit(1)
        else:
            print(" Returning...")
            print()
            pass
    else:
        print(" No updates available!")
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

def download(package):

    file = full_db[package]['file']

    link = urljoin("http://wunderwungiel.pl/MeeGo/openrepos/", file)
    print(" {}{}WAIT!{}{} Downloading...\n{}".format(red, blink, reset, red, reset))      
    try:
        response = urlopen(link)
        total_size_in_bytes = int(response.headers.get('Content-Length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        f = open(os.path.join("/home/user/MyDocs/", file), "wb")
        while True:
            data = response.read(block_size)
            if not data:
                break
            progress_bar.update(len(data))
            f.write(data)
        
        f.close()

        progress_bar.close()

    except (HTTPError, URLError):
        print(" {}Error while downloading content!{}".format(red, reset))
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        return

    print()
    print(" Saved {} in /home/user/MyDocs!\n".format(file))

def ovi_download(file, link, prompt=True, mydocs=False):
    print(" {}{}WAIT!{}{} Downloading...\n{}".format(red, blink, reset, red, reset))       
    try:
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
    except (HTTPError, URLError):
        print(" {}Error while downloading content!{}".format(red, reset))
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
        return
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

    display_name = full_db[package]['display_name']

    print(" Installing...")
    print(" ")

    command = 'LANG=C aegis-apt-get install -y --force-yes {}'.format(package)

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        result = result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        result = e.output
        result = result.decode("utf-8")
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

    print()
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
        depends = re.findall("depends on (.+)\s\(.+\);", result)
        if not depends:
            depends = re.findall("depends on (.+);", result)
        
        if not depends:
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

        depends_string = ', '.join(depends)
        print(" {} depends on following\n dependencies, not installed yet:\n\n {}.".format(display_name, depends_string))
        print()
        print(" Install them manually.")
     
    print()
    print(" {}{} installed!{}".format(green, display_name, reset))
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))


def uninstall(package):
    output = subprocess.call(
        "LANG=C aegis-apt-get autoremove --purge -y --force-yes {}".format(package),
        shell=True,
        stdout=open("/dev/null", "w")
    )
    if output != 0:
        print(" Something went wrong while uninstalling...\n Try uninstalling manually." )
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
    
def fix():
    
    subprocess.call("aegis-apt-get install -f", shell=True)
    input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

    
def add_repo():

    try:
        repo_dir = "/etc/apt/sources.list.d/wunderw-openrepos.list"
        repo_text = "deb http://wunderwungiel.pl/MeeGo/openrepos ./"

        pref_dir = "/etc/apt/preferences.d/wunderw-openrepos.pref"
        pref_text = """Package: *
Pin: origin wunderw-openrepos
Pin-Priority: 1"""

        if os.path.isdir(repo_dir):
            shutil.rmtree(repo_dir)
        elif os.path.isfile(repo_dir):
            os.remove(repo_dir)

        with open(repo_dir, "w") as f:
            f.write(repo_text)
    
        with open(pref_dir, "w") as f:
            f.write(pref_text)
    except Exception as e:
        return "Error"

def remove_repo():

    repo_dir = "/etc/apt/sources.list.d/wunderw-openrepos.list"

    pref_dir = "/etc/apt/preferences.d/wunderw-openrepos.pref"

    if os.path.isdir(repo_dir):
        shutil.rmtree(repo_dir)
    elif os.path.isfile(repo_dir):
        os.remove(repo_dir)
    if os.path.isdir(pref_dir):
        shutil.rmtree(pref_dir)
    elif os.path.isfile(pref_dir):
        os.remove(pref_dir)

def is_repo_enabled():
    repo_dir = "/etc/apt/sources.list.d/wunderw-openrepos.list"
    repo_text = "deb http://wunderwungiel.pl/MeeGo/openrepos ./"

    pref_dir = "/etc/apt/preferences.d/wunderw-openrepos.pref"
    pref_text = """Package: *
Pin: origin wunderw-openrepos
Pin-Priority: 1"""

    if not os.path.isfile(repo_dir):
        return False
    if not os.path.isfile(pref_dir):
        return False

    with open(repo_dir, "r") as f:
        file_text = f.read()
        if file_text != repo_text:
            return False
    with open(pref_dir, "r") as f:
        file_text = f.read()
        if file_text != pref_text:
            return False
    return True