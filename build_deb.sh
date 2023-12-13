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
rm -rf lib/__pycache__

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

mkdir -p {DEBIAN,usr/share,opt/MeeShop/bin}
mkdir -p usr/share/{icons/hicolor/80x80/apps,applications}

cat > usr/share/applications/MeeShop.desktop <<EOF
#!/usr/bin/env xdg-open
[Desktop Entry]
Type=Application
Name=MeeShop
Categories=System;
Exec=/usr/bin/invoker --splash=/opt/MeeShop/splash.png --type=e /usr/bin/meego-terminal -n -e /usr/bin/aegis-exec -s -u user -l "/opt/MeeShop/bin/MeeShop"
Icon=/usr/share/icons/hicolor/80x80/apps/MeeShop80.png
EOF

cat > opt/MeeShop/bin/MeeShop <<EOF
#!/bin/sh

cd /opt/MeeShop
./main.py && exit 0

echo "Please Enter to exit..."
read
exit 0
EOF

cp ../res/icon80.png usr/share/icons/hicolor/80x80/apps/MeeShop80.png
cp ../res/splash.png opt/MeeShop/

cp ../main.py opt/MeeShop
cp -r ../lib opt/MeeShop/

package="meeshop"
version="$1"
arch="armel"
maintainer="Wunder Wungiel <me@wunderwungiel.pl>"
size=$(LANG=C du -c opt usr | grep total | awk '{print $1}')
depends="wunderw-python3.11-opt (= 3.11.3-0)"
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

cat > DEBIAN/control <<EOF
Package: $package
Version: $version
Architecture: $arch
Maintainer: $maintainer
Installed-Size: $size
Depends: $depends
Section: $section
Priority: optional
Homepage: $homepage
Description: $description
Aegis-Manifest: included
Maemo-Display-Name: $display_name
Maemo-Flags: visible
Maemo-Icon-26:
$icon2
EOF

rm -f ../md5
find -type f | grep -v "./DEBIAN" > ../md5
while read line; do if [ -f "$line" ]; then line=`echo "$line" | cut -c 3-`; md5sum "$line" >> DEBIAN/md5sums; echo S 15 com.nokia.maemo H 40 `sha1sum "$line" | cut -c -40` R `expr length "$line"` $line >> DEBIAN/digsigsums; fi; done < "../md5"
rm -f ../md5

cp ../control/* DEBIAN/

cd ..

filename="$package"_"$version"_"$arch".deb
dpkg-deb -b --root-owner-group -Zgzip tmp/ $filename > /dev/null

ar r "$filename" _aegis

rm -rf tmp

echo -e "$green"Package "$package" created. Output: "$cyan""$filename""$reset"
