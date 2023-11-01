import requests
import re
from bs4 import BeautifulSoup

class AppInfo:
    def __init__(self, title, description, stars, screenshots, files, author, icon):
        self.title = title
        self.description = description
        self.stars = stars
        self.screenshots = screenshots
        self.files = files
        self.author = author
        self.icon = icon

def get_right_link(link):
    link = link.strip()
    if not link.startswith("https://") and not link.startswith("http://"):
        link = "http://" + link
    if link.startswith("https://"):
        link = link.replace("https://", "http://")
    link = re.sub(r"^http://(www\.)?", 'http://', link)
    return link

def get_app_info(link):
    link = get_right_link(link)

    response = requests.get(link)
    text_content = response.text
    if response.status_code != 200:
        raise Exception(f"Error! Status code: {response.status_code}")
    soup = BeautifulSoup(text_content, 'html.parser')

    title = get_title(soup)
    description = get_description(soup)
    stars = get_stars(soup)
    screenshots = get_screenshots(soup)
    files = get_file_links(soup)
    author = get_author_name(soup)
    icon = get_icon(soup)

    return AppInfo(title, description, stars, screenshots, files, author, icon)
    

def get_title(soup):

    title_match = soup.find('h1', {'class': 'title', 'id': 'page-title'})
    if title_match:
        title = title_match.text
    if title:
        title = title.strip()
    else:
        title = None
    return title

def get_description(soup):

    div1_match = soup.find('div', {'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
    if not div1_match:
        return None
    div2_match = div1_match.find('div', {'class': 'field-items'})
    if not div2_match:
        return None
    div3_match = div2_match.find('div', {'class': 'field-item even', 'property': 'content:encoded'})
    if not div3_match:
        return None
    description = div3_match.text
    if not description:
        return None
    description = description.strip()
    return description

def get_stars(soup):

    div1_match = soup.find('div', {'class': 'fivestar-oxygen'})
    if not div1_match:
        return None
    div2_match = div1_match.find('div', {'class': 'fivestar-widget-static fivestar-widget-static-vote fivestar-widget-static-5 clearfix'})
    if not div1_match:
        return None
    stars_divs = {}
    stars = {}
    
    stars_divs["1"] = div2_match.find('div', {'class': 'star star-1 star-odd star-first'})
    stars_divs["2"] = div2_match.find('div', {'class': 'star star-2 star-even'})
    stars_divs["3"] = div2_match.find('div', {'class': 'star star-3 star-odd'})
    stars_divs["4"] = div2_match.find('div', {'class': 'star star-4 star-even'})
    stars_divs["5"] = div2_match.find('div', {'class': 'star star-5 star-odd star-last'})

    if all(value == "None" for value in stars_divs.values()):
        return None

    for key, value in stars_divs.items():
        span_match = value.find('span', {'class': 'on'})
        if span_match:
            stars[key] = "on"
        else:
            stars[key] = "off"
    return stars

def get_icon(soup):

    div1_match = soup.find('div', {'class': 'field field-name-field-icon field-type-image field-label-hidden'})
    if not div1_match:
        return None
    div2_match = div1_match.find('div', {'class': 'field-items'})
    if not div2_match:
        return None
    div3_match = div2_match.find('div', {'class': 'field-item even'})
    if not div3_match:
        return None
    img_match = div3_match.find('img')
    if not img_match:
        return None
    
    image = img_match.get('src')
    if not image:
        return None
    else:
        image = get_right_link(image)
        image = re.sub(r'\?itok=.*$', '', image)
        return image

def get_screenshots(soup):

    div1_match = soup.find('div', {'class': 'field-label'}, text="Screenshots: ")
    if not div1_match:
        return None
    div2_match = div1_match.find_next_sibling('div', {'class': 'field-items'})
    if not div2_match:
        return None
    div2_matches = div2_match.find_all('div', class_=re.compile(r'.*field-item.*'))
    if not div2_matches:
        return None
    
    screenshots = []

    for i, match in enumerate(div2_matches, start=1):
        a_match = match.find('a', class_=re.compile(r'.*colorbox.*'))
        if not a_match:
            continue
        else:
            link = a_match.get('href')
            if not link:
                continue
            else:
                link = get_right_link(link)    
                screenshots.append(link)

    if not screenshots:
        screenshots = None

    return screenshots

def get_file_links(soup):

    div1_match = soup.find('div', {'class': 'field-label'}, text="Application versions: ")
    if not div1_match:
        return None
    div2_match = div1_match.find_next_sibling('div', {'class': 'field-items'})
    if not div2_match:
        return None
    div3_match = div2_match.find('div', {'class': 'field-item even'})
    if not div3_match:
        return None
    table_match = div3_match.find('table', {'class': 'sticky-enabled'})
    if not table_match:
        return None
    tbody_match = table_match.find('tbody')
    if not tbody_match:
        return None
    tr_match_odd = tbody_match.find_all('tr', {'class': 'odd'})
    tr_match_even = tbody_match.find_all('tr', {'class': 'even'})

    if not tr_match_odd and not tr_match_even:
        return None

    if tr_match_odd:
        if tr_match_even:
            tr_match = tr_match_odd + tr_match_even
        else:
            tr_match = tr_match_odd
    elif tr_match_even:
        tr_match = tr_match_even

    files = {}

    for tr in tr_match:
        td_match = tr.find('td')
        span_match = td_match.find('span', {'class': 'file'})
        a_match = span_match.find('a')
        filename = a_match.text
        filelink = a_match.get('href')
        files[filename] = filelink
    
    if not files:
        files = None
    return files

def get_author_name(soup):

    div1_match = soup.find('div', {'class': 'meta submitted'})
    if not div1_match:
        return None
    span_match = div1_match.find('span', {'property': 'dc:date dc:created'})
    if not span_match:
        return None
    a_match = span_match.find('a', {'class': 'username'})
    if not a_match:
        return None
    
    author_name = a_match.text

    if not author_name:
        author_name = None
    
    return author_name