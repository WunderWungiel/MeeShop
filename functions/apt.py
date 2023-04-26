import subprocess
from urllib.request import urlopen
from urllib.parse import urljoin
from .tqdm import tqdm
import os
import re

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

class Apt:
    def meeshop_update(self, db):
        if self.check_update(package='meeshop', db=db):
            print(" Update available, please download using MeeShop itself")
        else:
            print(" No updates available!")
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

    def download(self, file, prompt=True, mydocs=False):
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

    def ovi_download(self, file, link, prompt=True, mydocs=False):
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

    def install_dict(self, packages):
        packages = list(packages)
        installed = {}
        for package in packages:
            installed[package] = self.is_installed(package)
        return installed

    def check_update(self, package, db):
        try:
            result = subprocess.check_output("LANG=C dpkg-query -s {}".format(package), shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            result = e.output
        result = result.decode("utf-8")
        version = re.search("Version: (.+)", result)
        if not version:
            return "Error"
        version = version.group(1)
        if version != db[package]['version']:
            return True
        else:
            return False

    def is_installed(self, package):
        try:
            result = subprocess.check_output("LANG=C dpkg-query -s {}".format(package), shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            result = e.output
        result = result.decode("utf-8")
        if re.search("Status:.*ok installed.*", result):
            return True
        else:
            return False

    def install(self, display_name, filename):

        print(" Installing...")
        print(" ")
        filepath = os.path.join("/opt/MeeShop/.cache", filename)
        command = 'LANG=C aegis-dpkg -i "{}"'.format(filepath)
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            result = e.output
        result = result.decode("utf-8")
        depends = re.findall("depends on (.+);", result)
        if depends:
            depends = ', '.join(depends)
            print(" Package {} depends on following\n dependencies, not installed yet:\n\n {}.\n\n Try APT Fixer from main menu - if it fails, then search for missing packages\n in MeeShop.".format(display_name, depends))

        print(" ")
        print(" {}{} installed!{}".format(green, display_name, reset))
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

    def uninstall(self, package):
        output = subprocess.call(
            "LANG=C dpkg -r {}".format(package),
            shell=True,
            stdout=open("/dev/null", "w")
        )
        if output != 0:
            print(" Something went wrong while uninstalling...\n Try uninstalling manually." )
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))
    
    def fix(self):
        subprocess.call("aegis-apt-get install -f", shell=True)
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))



"""def install_apt(package):
    result = subprocess.run("aegis-apt-get install -y {}".format(package), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(" Package \"{}\" doesn't seem to exist in standard repos...".format(package))
        print(" Trying installing from MeeShop repository, please wait...")
        time.sleep(2)
        return False
    else:
        return True
    
def install_meeshop(db, package):
    if package not in db.keys():
        return "not_in_db"
    display_name = db[package]['package']
    filename = db[package]['file']
    link = "wunderwungiel.pl/MeeGo/openrepos/" + db[package]['file']
    link = quote(link)
    link = "http://" + link
    _ = install(link=link, display_name=display_name, filename=filename)
    if _ == "success":
        return "success"
    else:
        return "false\""""
    
