#!/bin/bash

blue='\033[96m'
red='\033[31m'
reset='\033[0m'
green='\033[32m'
blink='\033[5m'
yellow='\033[33m'
cyan='\033[1;36m'

set -e

rm -rf tmp *.deb
rm -rf lib/__pycache__ lib/tqdm/__pycache__

if ! command -v dpkg-deb > /dev/null 2>&1; then
    echo -e " $red"dpkg-dev not available..."$reset"
    exit 0
fi

if [[ -z $1 ]] || [[ $1 == "" ]]; then
    echo -e " $red"Provide version as argument..."$reset"
    exit 0
fi

mkdir tmp
cd tmp

mkdir -p {DEBIAN,usr/share,opt/MeeShop}
mkdir -p usr/share/{icons/hicolor/80x80/apps,applications}

cp ../MeeShop.desktop usr/share/applications/

cp ../res/icon80.png usr/share/icons/hicolor/80x80/apps/MeeShop80.png
cp ../res/splash.png opt/MeeShop/

cp ../main.py opt/MeeShop
cp -r ../lib opt/MeeShop/

package="meeshop"
version="$1"
arch="armel"
maintainer="Wunder Wungiel <dredlok706@yandex.com>"
size=$(LANG=C du -c opt usr | grep total | awk '{print $1}')
depends="python3, python3.1"
section="user/system"
homepage="http://wunderwungiel.pl"
description="App store for Nokia N9, built upon Python"
display_name="MeeShop"

icon=$(base64 ../res/icon80.png)
icon2=""

IFS=$'\n'

for line in $icon; do
    icon2+=" $line\n"
done

echo -e "Package: $package\nVersion: $version\nArchitecture: $arch\nMaintainer: $maintainer\nInstalled-Size: $size\nDepends: $depends\nSection: $section\nPriority: optional\nHomepage: $homepage\nDescription: $description\nAegis-Manifest: included\nMaemo-Display-Name: $display_name\nMaemo-Flags: visible\nMaemo-Icon-26:\n$icon2" > DEBIAN/control

files="$(find opt -type f)"
files2="$(find usr -type f)"

echo "$files" | while IFS= read -r line; do

    if [ -f "$line" ]; then
        echo "S 15 com.nokia.maemo H 40 $(sha1sum "$line" | cut -c -40) R $(expr length "$line") $line" >> DEBIAN/digsigsums
    fi
done

echo "$files2" | while IFS= read -r line; do

    if [ -f "$line" ]; then
        echo "S 15 com.nokia.maemo H 40 $(sha1sum "$line" | cut -c -40) R $(expr length "$line") $line" >> DEBIAN/digsigsums
    fi
done

echo "$files" | while IFS= read -r line; do

    result=$(md5sum "$line")

    if [ -f "$line" ]; then
        echo "$result" >> DEBIAN/md5sums
    fi
done

echo "$files2" | while IFS= read -r line; do

    result=$(md5sum "$line")

    if [ -f "$line" ]; then
        echo "$result" >> DEBIAN/md5sums
    fi
done

cp ../control/* DEBIAN/

cd ..

filename="$package"_"$version"_"$arch".deb
dpkg-deb -b --root-owner-group -Zgzip tmp/ $filename > /dev/null
ar r "$filename" _aegis

rm -rf tmp

echo -e "$green"Package "$package" created. Output: "$cyan""$filename""$reset"