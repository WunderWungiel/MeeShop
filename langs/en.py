blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

class Categories:
    def applications(self):
        return "Applications"
    def games(self):
        return "Games"
    def personalisation(self):
        return "Personalisation"

class Strings:
    
    def __init__(self):
        pass

    categories = Categories()

    def press_enter_to_continue(self):
        input(" {}{}Press Enter to continue... {}".format(blink, cyan, reset))

    def something_wrong_with_internet_connection(self):
        print(" {}Something wrong with internet connection.{}".format(red, reset))

    def aegis_hack_not_found(self):
        print(" {}Aegis-install hack by CODeRUS needs to be installed.{}".format(red, reset))
        print(" Get it here:")

    def about(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |      MeeShop© 2023 WunderWungiel     |")
        print(" |                                      |")
        print(" |      App store for MeeGo Harmattan   |")
        print(" |      written using Python 3.1.       |")
        print(" |                                      |")
        print(" |      Special thanks to:              |")
        print(" |                                      |")
        print(" |        - Yaroslav Chepel             |")
        print(" |            (icon designer)           |")
        print(" |                                      |")
        print(" |      Join our Telegram group:        |")
        print(" |                                      |")
        print(" |    https://t.me/linuxmobile_world    |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def category_selection_list(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |         Welcome to {}MeeShop{}!          |".format(cyan, reset))
        print(" |                                      |")
        print(" |       {}Select category / option{}       |".format(blink, reset))
        print(" |                                      |")
        print(" |         1. Applications              |")
        print(" |         2. Games                     |")
        print(" |         3. Personalisation           |")
        print(" |                                      |")
        print(" |         4. RSS Feeds                 |")
        print(" |         5. APT fixer                 |")
        print(" |                                      |")
        print(" |         6. Change language           |")
        print(" |         7. About                     |")
        print(" |                                      |")
        print(" |         0. Exit                      |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def wrong_number(self):
        print(" {}Wrong number, select a correct one!{}".format(red, reset))

    def options_selection_list(self, name):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |         Welcome to {}MeeShop{}!          |".format(cyan, reset))
        print(" |                                      |")
        if len(name) % 2 != 0:
            name = name + " "
        lenght = " " * int((38 - len(name)) / 2) 
        print(" |{}{}{}{}{}{}|".format(lenght, blink, cyan, name, reset, lenght))
        print(" |                                      |")
        print(" |          Select an option:           |")
        print(" |                                      |")
        print(" |             1. Search                |")
        print(" |             2. Show apps             |")
        print(" |             3. Return                |")
        print(" |                                      |")
        print(" |             0. Exit                  |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def enter_query_0(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |        Enter query, 0 to return:     |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def query_to_search(self):
        query = input(" {}Query to search:{} ".format(yellow, reset))
        return query
    
    def show_apps_list(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |           List of packages:          |")
        print(" |                                      |")

    def rss_feeds(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |              RSS feeds:              |")    
        print(" |                                      |")

    def rss_feeds_return(self):
        print(" |                                      |")
        print(" |          0. Return                   |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def select_a_country_digit(self):
        country = input(" {}Select a country (digit):{} ".format(yellow, reset))
        return country
    
    def feeds_for(self, country_name):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |           Feeds for {}:          |".format(country_name))
        print(" |                                      |")

    def feeds_for_return(self):
        print(" |                                      |")
        print(" |     0. Return                        |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def select_a_feed(self):
        selected = input(" {}Select a feed:{} ".format(yellow, reset))
        return selected
    
    def no_apps_found(self):
        print(" {}No apps found!{}".format(red, reset))

    def search_results(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |            Search results:           |")
        print(" |                                      |")

    def ask_for_results(self):
        ask = input(" {}Type numbers, ALL or 0:{} ".format(yellow, reset))
        return ask
    
    def wait_downloading(self):
        print(" {}{}WAIT!{}{} Downloading...\n{}".format(red, blink, reset, red, reset))

    def saved(self, filename):
        print(" Saved {}!\n".format(filename))
    
    def installing(self):
        print(" Installing...")

    def installed(self, pkg):
        print(" {}{} installed!{}".format(green, pkg, reset))

    def change_language(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |         Welcome to {}MeeShop{}!          |".format(cyan, reset))
        print(" |                                      |")
        print(" |       {}Select desired language:{}       |".format(blink, reset))
        print(" |                                      |")
        print(" |         1. English                   |")
        print(" |         2. Русский                   |")
        print(" |                                      |")
        print(" |         0. Return                    |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def input_your_language(self):
        language = input(" {}Type number of desired language:{} ".format(cyan, reset))
        return language
    
    def restart_app(self):
        print(" {}MeeShop will be closed to load new language.\n Open it again then.{}".format(cyan, reset))