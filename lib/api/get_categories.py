import re
import requests
from bs4 import BeautifulSoup

def get_right_link(link):
    link = link.strip()
    if not link.startswith("https://") and not link.startswith("http://"):
        link = "http://" + link
    if link.startswith("https://"):
        link = link.replace("https://", "http://")
    link = re.sub(r"^http://(www\.)?", 'http://', link)
    return link

def get_categories():

    link = "https://openrepos.net"

    response = requests.get(link)
    text_content = response.text
    if response.status_code != 200:
        raise Exception(f"Error! Status code: {response.status_code}")
    soup = BeautifulSoup(text_content, 'html.parser')

    categories = {}

    cats_div_match = soup.find('div', {'id': 'block-menu-menu-categories', 'class': 'block block-menu'})
    cats_div2_match = cats_div_match.find('div', {'class': 'content'})
    cats_ul_match = cats_div2_match.find('ul', {'class': 'menu clearfix'})
    cats_li_matches = cats_ul_match.find_all('li')
    
    for li in cats_li_matches:
        a_match = li.find('a')
        category = a_match.text
        link = a_match.get('href')
        if not link:
            continue
        link = "http://openrepos.net" + link
        categories[category] = {'link': link}

        small_cats_ul_match = li.find('ul', {'class': 'menu clearfix'})
        if not small_cats_ul_match:
            continue
        small_cats_li_matches = small_cats_ul_match.find_all('li')
        if not small_cats_li_matches:
            continue
        
        categories[category]['categories'] = {}

        for small_cats_li in small_cats_li_matches:
            small_cat_a_match = small_cats_li.find('a')
            if not small_cat_a_match:
                continue
            small_cat = small_cat_a_match.text
            if not small_cat:
                continue
            small_link = small_cat_a_match.get('href')
            if not small_link:
                continue
            small_link = "http://openrepos.net" + small_link
            categories[category]['categories'][small_cat] = small_link

    return categories