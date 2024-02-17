import subprocess
import os
import re
from urllib.parse import urljoin

from .tui import rprint
from .dbc import categories
from .small_libs import quit, reset, red, blink, cyan, press_enter, download_file

full_db = categories["full"]["db"]

#folder = "."
folder = "/home/user/MyDocs"

def update():
    try:
        process = subprocess.run(["/opt/MeeShop/scripts/update"])
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
    
# Check if dpkg status area is locked.
def is_dpkg_locked():
    paths = [
        "/var/lib/dpkg/lock",
        "/var/lib/apt/lists/lock"
    ]

    # We check each file in paths, if it's being used by apt-get or dpkg.
    for path in paths:


        if not os.path.isfile(path):
            continue

        try:
            # The lsof does its job. We also pass LANG=C to make sure it's English.
            process = subprocess.run(["lsof", path], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # PermissionError is raised if lsof can't be launched because of permissions.
        except PermissionError:
            rprint(f"{red} A problem with file permissions.{reset}")
            press_enter()
            return
        # While FileNotFoundError is raised if "lsof" doesn't exist at all.
        except FileNotFoundError:
            rprint(f"{red} File not found.{reset}")
            press_enter()
            return
        
        result = process.stdout

        # Here is the check for dpkg / apt-get in output.
        if "dpkg.real" in result or "apt-get.real" in result:
            return True
    
    return False

def meeshop_update():
    status = check_update('meeshop')
    if status == "Error":
        return "Error"
    if status:
        answer = input(f"{cyan} Update available, wanna update now?{reset} ")
        if answer.lower() in ["y", "yes"]:
            try:
                install("meeshop")
            except Exception as e:
                print(f" Error {red}{e}{reset}! Report to developer.")
                input(f"{blink}{cyan} Press Enter to exit... {reset}")
                quit()
        else:
            print(" Returning...")
            print()
            pass
    else:
        print(" No updates available!")
    press_enter()

def download(package):

    file = full_db[package]['file']
    filename = os.path.basename(file)

    link = urljoin("http://wunderwungiel.pl/MeeGo/openrepos/", file)
    download_file(link=link, filename=filename, prompt=True)

def check_update(package):
    try:
        process = subprocess.run(["/opt/MeeShop/scripts/dpkg-query", package], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
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
    return False
    process = subprocess.run(["/opt/MeeShop/scripts/dpkg-query", package], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    result = process.stdout
    if re.search("Status:.*ok installed.*", result):
        return True
    else:
        return False

def install(package):

    display_name = full_db[package]['display_name']
    version = full_db[package]['version']

    print(" Installing...")
    print(" ")

    try:
        process = subprocess.run(["/opt/MeeShop/scripts/install", package], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
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
    press_enter()

def dpkg_install(display_name, filename):

    print(" Installing...")
    print(" ")
    filepath = os.path.join("/opt/MeeShop/.cache", filename)
    try:
        process = subprocess.run(["/opt/MeeShop/scripts/dpkg_install", filepath], env={'LANG': 'C'}, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
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
        print(f" {display_name} depends on following\n dependencies, not installed yet:\n\n {depends_string}.")
        print()
        print(" Install them manually.")
     
    print()
    press_enter()

def uninstall(package):
    try:
        output = subprocess.call(
            ["/opt/MeeShop/scripts/uninstall", package],
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
        subprocess.call(["/opt/MeeShop/scripts/fix"])
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

        if os.path.isfile(repo_dir):
            os.remove(repo_dir)

        with open(repo_dir, "w") as f:
            f.write(repo_text)
    
        with open(pref_dir, "w") as f:
            f.write(pref_text)
    except:
        return "Error"

def remove_repo():

    repo_dir = "/etc/apt/sources.list.d/wunderw-openrepos.list"

    pref_dir = "/etc/apt/preferences.d/wunderw-openrepos.pref"

    if os.path.isfile(repo_dir):
        os.remove(repo_dir)
    if os.path.isfile(pref_dir):
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