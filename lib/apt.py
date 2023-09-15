import subprocess
import sys
import os
import re
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError, URLError
import shutil
from . import dbc
from .tui import rprint, press_enter
try:
    from tqdm import tqdm
except ImportError:
    print(" tqdm not installed.")
    press_enter()
    sys.exit(1)

db_creator = dbc.Db_creator()
ovi_db = db_creator.ovi_db
categories = db_creator.categories
full_db = categories["full"]["db"]

folder = "."
#folder = "/home/user/MyDocs"

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def update():
    try:
        process = subprocess.run(["apt-get", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except PermissionError:
        rprint(f"{red} A problem with file permissions.{reset}")
        press_enter()
        return "Error"
    except FileNotFoundError:
        rprint(f"{red} File not found.{reset}")
        press_enter()
        return "Error"
    if process.returncode != 0:
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
            process = subprocess.run(["lsof", path], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        except PermissionError:
            rprint(f"{red} A problem with file permissions.{reset}")
            press_enter()
            return
        except FileNotFoundError:
            rprint(f"{red} File not found.{reset}")
            press_enter()
            return
        
        result = process.stdout

        if "dpkg.real" in result or "apt-get.real" in result:
            return True
    
    return False

def meeshop_update():
    status = check_update('meeshop')
    if status == "Error":
        return "Error"
    if status:
        answer = input("{} Update available, wanna update now?{} ".format(cyan, reset))
        if answer.lower() in ["y", "yes"]:
            try:
                install("meeshop")
            except Exception as e:
                print(" Error {}{}{}! Report to developer.".format(red, e, reset))
                input("{}{} Press Enter to exit... {}".format(blink, cyan, reset))
                sys.exit(1)
        else:
            print(" Returning...")
            print()
            pass
    else:
        print(" No updates available!")
    press_enter()

def download(package):

    file = full_db[package]['file']

    link = urljoin("http://wunderwungiel.pl/MeeGo/openrepos/", file)
    print(" {}{}WAIT!{}{} Downloading...\n{}".format(red, blink, reset, red, reset))      
    try:
        response = urlopen(link)
        total_size_in_bytes = int(response.headers.get('Content-Length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        f = open(os.path.join(folder, file), "wb")
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
        press_enter()
        return

    print()
    print(" Saved {} in {}!\n".format(file, folder))

def ovi_download(file, link, prompt=True, mydocs=False):
    print(" {}{}WAIT!{}{} Downloading...\n{}".format(red, blink, reset, red, reset))       
    try:
        response = urlopen(link)
        total_size_in_bytes = int(response.headers.get('Content-Length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        if mydocs:
            f = open(os.path.join(folder, file), "wb")
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
        press_enter()
        return
    print()
    if prompt:
        if not mydocs:
            print(" Saved {} in /opt/MeeShop/.cache!\n".format(file))
        else:
            print(" Saved {} in {}!\n".format(file, folder))

def check_update(package):
    try:
        process = subprocess.run(["LANG=C", "dpkg-query", "-s", package], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except PermissionError:
        rprint(f"{red} A problem with file permissions.{reset}")
        press_enter()
        return "Error"
    except FileNotFoundError:
        rprint(f"{red} File not found.{reset}")
        press_enter()
        return "Error"
    result = process.stdout
    version = re.search("Version: (.+)", result)
    if not version:
        return "Error"
    version = version.group(1)
    if version < full_db[package]['version']:
        return True
    else:
        return False

def is_installed(package):
    process = subprocess.run(["dpkg-query", "-s", package], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    result = process.stdout
    if re.search("Status:.*ok installed.*", result):
        return True
    else:
        return False

def install(package):

    display_name = full_db[package]['display_name']

    print(" Installing...")
    print(" ")

    try:
        process = subprocess.run(["aegis-apt-get", "install", "-y", "--force-yes", package], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except PermissionError:
        rprint(f"{red} A problem with file permissions.{reset}")
        press_enter()
        return
    except FileNotFoundError:
        rprint(f"{red} File not found.{reset}")
        press_enter()
        return
    result = process.stdout
    if process.returncode != 0:
        print(" Some error occured... Output:")
        print()
        print(" ########################################")
        print()
        print(result)
        print()
        print(" ########################################")
        print()

        press_enter()
        return

    print()
    print(" {}{} installed!{}".format(green, display_name, reset))
    press_enter()

def ovi_install(display_name, filename):

    print(" Installing...")
    print(" ")
    filepath = os.path.join("/opt/MeeShop/.cache", filename)
    try:
        process = subprocess.run(["aegis-dpkg", "-i", filepath], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except PermissionError:
        rprint(f"{red} A problem with file permissions.{reset}")
        press_enter()
        return
    except FileNotFoundError:
        rprint(f"{red} File not found.{reset}")
        press_enter()
        return
    result = process.stdout
    if process.returncode != 0:
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

            press_enter()

            return

        depends_string = ', '.join(depends)
        print(" {} depends on following\n dependencies, not installed yet:\n\n {}.".format(display_name, depends_string))
        print()
        print(" Install them manually.")
     
    print()
    print(" {}{} installed!{}".format(green, display_name, reset))
    press_enter()


def uninstall(package):
    try:
        output = subprocess.call(
            ["aegis-apt-get autoremove", "--purge", "-y", "--force-yes", package],
            env={'LANG': 'C'}
        )
    except PermissionError:
        rprint(f"{red} A problem with file permissions.{reset}")
        press_enter()
        return
    except FileNotFoundError:
        rprint(f"{red} File not found.{reset}")
        press_enter()
        return
    if output != 0:
        print(" Something went wrong while uninstalling...\n Try uninstalling manually." )
    press_enter()
    
def fix():
    
    try:
        subprocess.call(["aegis-apt-get", "install", "-f"])
    except PermissionError:
        rprint(f"{red} A problem with file permissions.{reset}")
        press_enter()
        return
    except FileNotFoundError:
        rprint(f"{red} File not found.{reset}")
        press_enter()
        return
    press_enter()

    
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