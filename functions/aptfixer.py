import subprocess

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def apt_fixer():
    subprocess.call("aegis-apt-get install -f", shell=True)
    input(" \n {}{}Press any key to continue...{}".format(blink, cyan, reset)) 
