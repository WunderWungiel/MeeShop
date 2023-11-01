import requests
import re
from bs4 import BeautifulSoup

class SearchResults:
    def __init__(self, results, pages, current_page):
        self.results = results
        self.pages = pages
        self.current_page = current_page

def get_right_link(link):
    link = link.strip()
    if not link.startswith("https://") and not link.startswith("http://"):
        link = "http://" + link
    if link.startswith("https://"):
        link = link.replace("https://", "http://")
    link = re.sub(r"^http://(www\.)?", 'http://', link)
    link = re.sub(r'/?$', '', link)
    return link

def search(query):
    
    if len(query) <= 3:
        raise Exception("Search query should be 3-letters long or more.")
    
    link = f"http://openrepos.net/search/node/{query}"
    
    response = requests.get(link)
    text_content = response.text

    soup = BeautifulSoup(text_content, 'html.parser')
    
    if soup.find('h2', text='Your search yielded no results'):
        return None

    result = get_search_results(soup)
    search_results, current_pages_dict, pages = result
    return SearchResults(search_results, pages, current_pages_dict)
    

def get_search_results(soup):

    search_results = {}

    h2_match = soup.find('h2', text='Search results')
    ol_match = h2_match.find_next_sibling('ol', {'class': 'search-results node-results'})
    li_matches = ol_match.find_all('li', {'class': 'search-result'})
    for li in li_matches:
        title_h3_match = li.find('h3', {'class': 'title'})
        title_a_match = title_h3_match.find('a')
        if not title_a_match:
            continue
        title = title_a_match.text.strip()
        link = title_a_match.get('href').strip()
        search_results[title] = {'link': link}

        content_div_match = li.find('div', {'class': 'search-snippet-info'})
        content_description_p_match = content_div_match.find('p', {'class': 'search-snippet'})
        description = content_description_p_match.text.strip()
        description_lines = [line.strip() for line in description.splitlines()]
        description_lines = [line for line in description_lines if line != '']
        description = "\n".join(description_lines)
        for word in ("Category:", "Screenshots:", "Keywords:"):
            description = re.sub('\s*{}\s*.*\s*'.format(word), '', description)
        description = re.sub(r'^\s*\.\.\.\s*', '', description)
        description = re.sub(r'\s*\.\.\.\s*.*$', '', description)
        description = re.sub(r'\d\.\d       \(  \d+   votes\)', '', description)
        description = re.sub(r'\(  \d+   votes\)', '', description)
        if re.search(r'\s*Attachment.*', description):
            description = re.sub(r'\s*Attachment.*\n.*', '', description, re.DOTALL)
        description = re.sub(r'\s*\.\.\.\s*.*$', '', description)
        description_lines = [line.strip() for line in description.splitlines()]
        description_lines = [line for line in description_lines if line != '']
        description = "\n".join(description_lines)
        description += " ..."

        search_results[title]['description'] = description

        content_info_p_match = content_div_match.find('p', {'class': 'search-info'})
        content_info_a_match = content_info_p_match.find('a', {'class': 'username'})
        username = content_info_a_match.text.strip()
        userlink = content_info_a_match.get('href').strip()
        userlink = "http://openrepos.net" + userlink
        search_results[title]['username'] = {username: userlink}

        date = content_info_p_match.text.replace(username, '').strip()
        date = re.sub(r'^- ', '', date)
        date = re.sub(r' -.*', '', date)
        search_results[title]['date'] = date

    pages = {}

    pages_ul_match = soup.find('ul', {'class': 'pager'})
    if not pages_ul_match:
        return (search_results, None, None)
    else:
        pages_li_matches = pages_ul_match.find_all('li')
        for li in pages_li_matches:
            if "pager-current" in li.get('class'):
                current_page_i = li.text
                current_page_link = "/search/node/meecast?page={}".format(str(int(current_page_i) - 1))
                continue
            pages_a_match = li.find('a')
            pages_i = pages_a_match.text
            pages_link = pages_a_match.get('href')
            pages_link = "http://openrepos.net" + pages_link
            pages[pages_i] = pages_link
        return (search_results, {current_page_i: current_page_link}, pages)