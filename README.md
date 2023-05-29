# MeeShop

**MeeShop** is a **brand-new**, **working** app store for Nokia N9 / N950 devices running MeeGo Harmattan. MeeShop uses [OpenRepos](http://openrepos.net) as its database.


 - [x] OpenRepos
 - [x] Ovi Store
 - [ ] Automatic dependencies resolving


## Installing

You need to have [Developer Mode](http://wunderwungiel.pl/MeeGo/posts/devmode-22.04.2023.html) enabled and [Aegis-hack](https://talk.maemo.org/showthread.php?t=90750).
Python needs to be installed. Run **Terminal**, and type following commands:

    devel-su
    (enter "rootme" without quotes as password)
    aegis-apt-get install python3 python3.1 -y --force-yes

Download latest release (`.deb` file) from [Releases](https://github.com/WunderWungiel/MeeShop/releases) page, and transfer it to N9, saving in **MyDocs** (i.e. **Nokia N9** drive when connected to PC).
Run the **Terminal** again, and type following commands:

    devel-su
    (enter "rootme" without quotes as password)
    cd /home/user/MyDocs
    aegis-dpkg -i meeshop_RELEASE_armel.deb
    (replace RELEASE with the proper number, i.e. 0.1.0)
If you don't see any errors, you're ready to use MeeShop!

## How to use

**MeeShop** is a **CLI** app with no native **GUI**. However, it has been designed to make the usage as easy as possible! You don't need to enter any commands.
Just **run MeeShop** from applications menu while being connected to Internet. You will see a retro-style menu with few options, like **Applications**. Below is a quick description of functions.

 - **Applications** - is the main function, which allows to search for apps and install them.
	 - **Search** - searches for apps
	 - **Show apps** - shows all available packages - *WIP*.
- **Ovi Store** - an innovative solution, allowing to search & install apps from the original **Ovi/Nokia Store**! Using Wayback Machine archiving system.
- **RSS Feeds** - a list of **working** RSS feeds for MeeGo, for selected countries.
- **APT Fixer** - runs simple `apt-get install -f` command, which can be used to fix some unresolved dependencies.
- **About** - name suggest the action.

Each function will ask you for something - you need to enter your "answer" and press **Enter** to confirm.
To **go back** (almost) anytime, press **0** when MeeShop asks you for something.

## Screenshots

## Credits

 - [IarChep / Ярослав](https://t.me/iaroslavchep) - icon, Russian translation and inexhaustible help and ingenuity!
 - [Python](https://python.org) for making an easy to learn, power programming language
 - [tqdm](https://github.com/tqdm/tqdm) developers for CLI progress bar
 - [Linux Mobile World](https://t.me/linuxmobile_world) community for testing this app
