blue = '\033[96m'
red = '\033[31m'
reset = '\033[0m'
green = '\033[32m'
blink = '\033[5m'
yellow = '\033[33m'
cyan = '\033[1;36m'

class Categories:
    def applications(self):
        return "Приложения"
    def games(self):
        return "Игры"
    def personalisation(self):
        return "Персонализация"

class Strings:
    
    def __init__(self):
        pass

    categories = Categories()

    def press_enter_to_continue(self):
        input(" {}{}Нажмите ввода, чтобы продолжить... {}".format(blink, cyan, reset))

    def something_wrong_with_internet_connection(self):
        print(" {}Проверьте подключение к интернету!{}".format(red, reset))

    def aegis_hack_not_found(self):
        print(" {}Установите Aegis-install hack от CODeRUS, чтобы продолжить!{}".format(red, reset))
        print(" Скачайте его здесь:")

    def about(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |      MeeShop© 2023 WunderWungiel     |")
        print(" |                                      |")
        print(" |        Магазин приложений для        |")
        print(" |      MeeGo Harmattan, написанный     |")
        print(" |            на Python 3.1.            |")
        print(" |                                      |")
        print(" |      Специальные благодарности:      |")
        print(" |                                      |")
        print(" |        - Ярослав Чепель              |")
        print(" |         (дизайнер иконок,            |")
        print(" |          (перевод на Русский)        |")
        print(" |                                      |")
        print(" |        Присоединяйтесь в нашу        |")
        print(" |           телеграмм группу:          |")
        print(" |                                      |")
        print(" |    https://t.me/linuxmobile_world    |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def category_selection_list(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |      Добро пожаловать в {}MeeShop{}!     |".format(cyan, reset))
        print(" |                                      |")
        print(" |       {}Выберите категорию / опцию{}     |".format(blink, reset))
        print(" |                                      |")
        print(" |         1. Приложения                |")
        print(" |         2. Игры                      |")
        print(" |         3. Персонализация            |")
        print(" |                                      |")
        print(" |         4. RSS Фиды                  |")
        print(" |         5. Фиксер APT                |")
        print(" |                                      |")
        print(" |         6. Изменить язык             |")
        print(" |         7. О MeeShop                 |")
        print(" |                                      |")
        print(" |         0. Выход                     |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def wrong_number(self):
        print(" {}Неправильная цифра пункта, выберите нужную!{}".format(red, reset))

    def options_selection_list(self, name):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |      Добро пожаловать в {}MeeShop{}!     |".format(cyan, reset))
        print(" |                                      |")
        if len(name) % 2 != 0:
            name = name + " "
        lenght = " " * int((38 - len(name)) / 2) 
        print(" |{}{}{}{}{}{}|".format(lenght, blink, cyan, name, reset, lenght))
        print(" |                                      |")
        print(" |        Выберите пункт / опцию:       |")
        print(" |                                      |")
        print(" |             1. Поиск                 |")
        print(" |             2. Показать пакеты       |")
        print(" |             3. Вернуться назад       |")
        print(" |                                      |")
        print(" |             0. Выход                 |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def enter_query_0(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |     Введите поисковый запрос. 0,     |")
        print(" |        чтобы вернуться назад         |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def query_to_search(self):
        query = input(" {}Поисковый запрос:{} ".format(yellow, reset))
        return query
    
    def show_apps_list(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |           Список пакетов:            |")
        print(" |                                      |")

    def rss_feeds(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |               RSS Фиды:              |")    
        print(" |                                      |")

    def rss_feeds_return(self):
        print(" |                                      |")
        print(" |          0. Вернуться назад          |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def select_a_country_digit(self):
        country = input(" {}Выберите страну (цифрой):{} ".format(yellow, reset))
        return country
    
    def feeds_for(self, country_name):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |           Фиды для {}:           |".format(country_name))
        print(" |                                      |")

    def feeds_for_return(self):
        print(" |                                      |")
        print(" |     0. Вернуться назад               |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def select_a_feed(self):
        selected = input(" {}Выберите фид:{} ".format(yellow, reset))
        return selected
    
    def no_apps_found(self):
        print(" {}приложения не найдены!{}".format(red, reset))

    def search_results(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |          Результаты поиска:          |")
        print(" |                                      |")

    def ask_for_results(self):
        ask = input(" {}Выпишите числа нужных приложений, ВСЁ или 0 для возврата:{} ".format(yellow, reset))
        return ask
    
    def wait_downloading(self):
        print(" {}{}ПОДОЖДИТЕ!{}{} Загрузка...\n{}".format(red, blink, reset, red, reset))

    def saved(self, filename):
        print(" Сохранен {}!\n".format(filename))
    
    def installing(self):
        print(" Установка...")

    def installed(self, pkg):
        print(" {}{} Установлен!{}".format(green, pkg, reset))

    def change_language(self):
        print("  -------------------------------------- ")
        print(" |                                      |")
        print(" |      Добро пожаловать в {}MeeShop{}!     |".format(cyan, reset))
        print(" |                                      |")
        print(" |       {}Выберите нужный вам язык:{}      |".format(blink, reset))
        print(" |                                      |")
        print(" |         1. English                   |")
        print(" |         2. Русский                   |")
        print(" |                                      |")
        print(" |         0. Return                    |")
        print(" |                                      |")
        print("  -------------------------------------- \n")

    def input_your_language(self):
        language = input(" {}Выпишите цифру, выбранного вами языка:{} ".format(cyan, reset))
        return language
    
    def restart_app(self):
        print(" {}MeeShop будет закрыт, чтобы установить новый язык.\n Откройте его самостоятельно.{}".format(cyan, reset))