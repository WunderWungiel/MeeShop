import requests
import re
from bs4 import BeautifulSoup

def get_right_link(link):
    link = link.strip()
    if not link.startswith("https://") and not link.startswith("http://"):
        link = "http://" + link
    if link.startswith("https://"):
        link = link.replace("https://", "http://")
    link = re.sub(r"^http://(www\.)?", 'http://', link)
    link = re.sub(r'/?$', '', link)
    return link

def get_site_apps(link=None, page=None, target=""):

    target = target.lower()

    if target and target not in ("harmattan_app", "maemo_app", "nemomobile_app", "sailfish_app", "pureos_app", "all"):
        raise Exception(" Bad target specified")

    if not link:
        if page:
            i = int(page) - 1
            if i == 0:
                link = f"https://openrepos.net/last-added-front"
            else:
                link = f"https://openrepos.net/last-added-front?page=0%2C{i}"
        else:
            raise TypeError("Missing argument: page / link")

    link = get_right_link(link)
    if target and target != "all":
        link += f"&view_content_types={target}"

    response = requests.get(link)
    text_content = response.text
    soup = BeautifulSoup(text_content, 'html.parser')
    apps = get_apps_list(soup)
    return apps
    
def get_apps_list(soup):
    
    
    div2_match = soup.find_all('div', {'class': 'view-content'})
    if not div2_match:
        return None
    else:
        div2_match = div2_match[-1]
    table_match = div2_match.find('table', {'class': 'views-view-grid cols-2'})
    tbody_match = table_match.find('tbody')
    tr_matches = tbody_match.find_all('tr')

    apps = {}

    for tr in tr_matches:
        td_matches = tr.find_all('td')
        for td in td_matches:
            title_div_match = td.find('div', {'class': 'views-field views-field-title'})
            if not title_div_match:
                continue
            title_span_match = title_div_match.find('span', {'class': 'field-content app-title'})
            if not title_span_match:
                continue
            title_a_match = title_span_match.find('a')
            if not title_a_match:
                continue

            title = title_a_match.text.strip()
            if not title:
                continue
            apps[title] = {}
            link = title_a_match.get('href')
            if link:
                apps[title]['link'] = "http://openrepos.net" + link

            stars_div_match = td.find('div', {'class': 'views-field views-field-field-rating-features'})
            icon_div_match = stars_div_match.find_next_sibling('div')
            if not icon_div_match:
                apps[title]['icon'] = None
            icon_div2_match = icon_div_match.find('div', {'class': 'app-icon'})
            if not icon_div2_match:
                apps[title]['icon'] = None
            icon_a_match = icon_div2_match.find('a')
            if not icon_a_match:
                apps[title]['icon'] = None
            icon_img_match = icon_a_match.find('img')
            if not icon_img_match:
                apps[title]['icon'] = None
            icon = icon_img_match.get('src')
            if not icon:
                apps[title]['icon'] = None
            else:
                icon = get_right_link(icon)
                icon = re.sub(r'\?itok=.*$', '', icon)
                apps[title]['icon'] = icon

            author_div_match = td.find('div', {'class': 'views-field views-field-name'})
            if not author_div_match:
                apps[title]['author'] = None
            author_span_match = author_div_match.find('span', {'class': 'field-content'})
            if not author_span_match:
                apps[title]['author'] = None
            author_a_match = author_span_match.find('a', {'class': 'username'})
            if not author_a_match:
                apps[title]['author'] = None
            author = author_a_match.text.strip()
            if author:
                apps[title]['author'] = author

    return apps
    