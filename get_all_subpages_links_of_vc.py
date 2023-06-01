import urllib.parse
from bs4 import BeautifulSoup
import random


# def load_user_agents():
#     try:
#         with open("user-agents.txt", 'r') as file:
#             return file.read().splitlines()
#     except FileNotFoundError:
#         print("user-agents.txt file not found.")
#         return []


# user_agents = load_user_agents()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0"


def get_vc_subpages_links(start_url, browser):
    visited_urls = set()
    links = []
    visited_urls.add(start_url)
    page = browser.new_page()
    page.set_extra_http_headers({"User-Agent": user_agent})
    page.goto(start_url)
    soup = BeautifulSoup(page.content(), 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href or href.startswith("mailto:"):
            continue
        abs_url = urllib.parse.urljoin(start_url, href)

        if abs_url.startswith("http://"):
            abs_url = abs_url.replace("http://", "https://")

        if abs_url.startswith('/') or abs_url.startswith("#"):
            abs_url = urllib.parse.urljoin(start_url, abs_url)

        if not abs_url.startswith(start_url) or not abs_url.startswith('https'):
            continue
        if abs_url in visited_urls:
            continue
        try:
            visited_urls.add(abs_url)
            links.append(abs_url)
        except Exception as e:
            print(e)
    return list(links)
