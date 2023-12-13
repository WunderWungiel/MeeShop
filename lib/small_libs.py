"""Copyright 2023 Wunder Wungiel

Small functions, that do not need additional files for each of them."""
import subprocess
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from tqdm import tqdm
import os
import re

bold = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'
cyan_background = '\033[48;5;104m'

# A very simple function, which just runs clear command.
# cls can be used on Windows instead.
def clean():
    subprocess.call(["clear"])

# pass as function
def passer():
    pass

def press_enter():
    input(f"{blink}{cyan} Press Enter to continue... {reset}")

# A direct replacement for sys.exit(status_code)
# This way doesn't require to import sys, and does exactly the same.
def quit(status_code=0):
    raise SystemExit(status_code)

def isodd(integer):

    if isinstance(integer, str):
        length = len(integer)
    elif isinstance(integer, (int, float, complex)):
        length = integer

    if length % 2 != 0:
        return True
    else:
        return False
    
def iseven(integer):
    if isodd(integer):
        return False
    else:
        return True

def about():

    print(" ┌──────────────────────────────────────┐")
    print(" │                                      │")
    print(" │      MeeShop© 2023 WunderWungiel     │")
    print(" │            Version: 0.3.0            │")
    print(" │                                      │")
    print(" │      App store for MeeGo Harmattan   │")
    print(" │      written using Python 3          │")
    print(" │                                      │")
    print(" │      Special thanks to:              │")
    print(" │                                      │")
    print(" │        - IarChep                     │")
    print(" │      (icon, inexhaustible help       │")
    print(" │       and ingenuity!)                │")
    print(" │        - Python                      │")
    print(" │        - LM World community          │")
    print(" │                                      │")
    print(" │      Join our Telegram group:        │")
    print(" │                                      │")
    print(" │    https://t.me/linuxmobile_world    │")
    print(" │                                      │")
    print(" └──────────────────────────────────────┘ \n")
    input(f"{blink}{cyan} Press Enter to continue... {reset}")

def download_file(link, folder=".", filename=None, prompt=True):
    print(f" {red}{blink}WAIT!{reset}{red} Downloading...\n{reset}")
    folder = "."
    folder = os.path.abspath(folder)
    try:
        r = urlopen(link)
        total_size_in_bytes = int(r.headers.get('Content-Length', 0))
        if not filename:

            # Try to get filename from Content-Disposition
            content_disposition = r.headers.get("Content-Disposition")
            if content_disposition:
                filename = re.findall("filename=(.+)", content_disposition)[0]
            else:
                parts = link.split('/')
                filename = parts[-1]

        path = os.path.join(folder, filename)
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        f = open(path, "wb")
        while True:
            data = r.read(1024)
            if not data:
                break
            progress_bar.update(len(data))
            f.write(data)
        
        f.close()
        progress_bar.close()

    except (HTTPError, URLError):
        print(f" {red}Error while downloading content!{reset}")
        press_enter()
        return
    if prompt:
        print()
        print(f" Saved {filename} in {folder}!\n")


# A primitive function to forcibly escape every RegEx-y character in variable.
def re_decoder(variable: str) -> str:
    variable = variable.replace("[", r"\[")
    variable = variable.replace("]", r"\]")
    variable = variable.replace(".", r"\.")
    variable = variable.replace("*", r"\*")
    variable = variable.replace("^", r"\^")
    variable = variable.replace("$", r"\$")
    variable = variable.replace("+", r"\+")
    variable = variable.replace("?", r"\?")
    variable = variable.replace("{", r"\{")
    variable = variable.replace("}", r"\}")
    variable = variable.replace("|", r"\|")
    variable = variable.replace("(", r"\(")
    variable = variable.replace(")", r"\)")
    variable = variable.replace("\A", r"\\A")
    variable = variable.replace("\b", r"\\b")
    variable = variable.replace("\B", r"\\B")
    variable = variable.replace("\d", r"\\d")
    variable = variable.replace("\D", r"\\D")
    variable = variable.replace("\s", r"\\s")
    variable = variable.replace("\S", r"\\S")
    variable = variable.replace("\w", r"\\w")
    variable = variable.replace("\W", r"\\W")
    variable = variable.replace("\Z", r"\\Z")
    return variable

# Remove duplicates from list
def remove_duplicates(_list: list) -> list:

    unique_elements = []

    for element in _list:
        if not element in unique_elements:
            unique_elements.append(element)
    
    return unique_elements

def split_item(text, width=38, space_left=9, i=1):
    i = str(i)
    i_length = len(i)
    text_length = len(text)

    parts = []

    #
    # First part
    #

    # Counting available space for first line.
    # width - space before i - 4 (two spaces * 2) - lenght of i

    first_available = width - space_left - 4 - i_length

    if text_length < first_available:
        left = first_available - text_length
        return [(text, left)]

    first_text = text[:first_available]
    first_text_length = len(first_text)

    first_left = first_available - first_text_length

    parts.append([first_text, first_left])

    _to_remove = text_length - first_available
    rest_of_text_all = text[-_to_remove:]

    #
    # Middle part
    #

    # Counting available space for second line.
    # width - 4 (two spaces * 2)
    middle_available = width - 4

    middle_parts = len(rest_of_text_all) // middle_available
    middle_text_length = (middle_parts * middle_available) + first_text_length

    start_index = first_text_length

    for part in range(middle_parts):
        
        end_index = start_index + middle_available
        part = text[start_index:end_index]
        start_index += middle_available

        parts.append([part, 0])

    #
    # Last part
    #

    last_index = text_length - middle_text_length
    last_text = text[-last_index:]
    last_text_length = len(last_text)
    last_left = width - 2 - last_text_length

    parts.append([last_text, last_left])

    return parts