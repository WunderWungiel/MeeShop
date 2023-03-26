import subprocess
import os

blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

def clean():
    subprocess.call("cls" if os.name == "nt" else "clear", shell=True) 