import asyncio
import time
import tldextract
import traceback
import urllib
from urllib.parse import urlparse

from playwright.async_api import async_playwright

from constants.constants import DELETE_URL_THAT_HAS_STRING, DELETE_URL_THAT_STARTS_WITH

def filter_link(link, main_website_domain, portfolio_url):
    if link == portfolio_url:
        return None

    if link.startswith(f"{portfolio_url}"):
        if not any(link.startswith(delete_url) for delete_url in DELETE_URL_THAT_STARTS_WITH) and not any(delete_url in link for delete_url in DELETE_URL_THAT_HAS_STRING):
            if link.startswith("http"):
                return link

    link_domain = urllib.parse.urlparse(link).netloc
    parsed_link1 = tldextract.extract(link_domain)
    parsed_link2 = tldextract.extract(main_website_domain)

    domain1 = parsed_link1.registered_domain
    domain2 = parsed_link2.registered_domain
    if domain1 != domain2:
        if not any(link.startswith(delete_url) for delete_url in DELETE_URL_THAT_STARTS_WITH) and not any(delete_url in link for delete_url in DELETE_URL_THAT_HAS_STRING):
            if link.startswith("http"):
                return link

    return None


# user_agents = load_user_agents()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0"


async def collect_links_with_playwright(url, starting_domain, browser):
    try:
        page = await browser.new_page()
        page.set_default_navigation_timeout(40000)
        await page.set_extra_http_headers({"User-Agent": user_agent})
        await page.goto(url)
        time.sleep(5)
        links = []
        elements = await page.query_selector_all('a')
        for element in elements:
            link = await element.get_attribute('href')
            filtered_link = filter_link(link, starting_domain, url)
            if filtered_link is not None:
                links.append(filtered_link)
            else:
                continue
        await page.close()
        return links
    except Exception as e:
        await page.close()
        print(e)
        traceback.print_exc()
        return None


async def collect_all_links(url, browser):
    starting_domain = urllib.parse.urlparse(url).netloc
    links = set()

    # Collect links using Playwright
    try:
        playwright_links = await collect_links_with_playwright(url, starting_domain, browser)
        if playwright_links is None:
            return None
        links.update(playwright_links)
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None
    return links


async def get_portfolio_links(url, browser):
    all_links = await collect_all_links(url, browser)
    if all_links is None:
        return None

    # Remove duplicate links
    unique_links = list(set(all_links))

    return unique_links