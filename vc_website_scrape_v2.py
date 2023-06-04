from bs4 import BeautifulSoup
import urllib.parse
import random

class Scraper:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0"
    async def scrape(self, url: str, browser) -> str:
        visited_urls = set()
        text = ""
        try:
            page = await browser.new_page()
            await page.set_extra_http_headers({"User-Agent": self.user_agent})
            text = await self.scrape_main(page, url, visited_urls)
            await page.close()
        except Exception as e:
            text = ""
            # print(e)
        return text

    @staticmethod
    async def extract_text(page, url: str) -> str:
        try:
            await page.goto(url)
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            return text
        except Exception as e:
            # print(e)
            return ""

    async def scrape_main(self, page, start_url, visited_urls):
        text = ""
        visited_urls.add(start_url)
        text += await self.extract_text(page, start_url)
        await page.goto(start_url)
        soup = BeautifulSoup(await page.content(), 'html.parser')
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
                text += await self.scrape_subpages(page, abs_url)
            except Exception as e:
                text = ""
                # print(e)
        return text

    @staticmethod
    async def scrape_subpages(page, url: str) -> str:
        text = ""
        text += await Scraper.extract_text(page, url)
        return text


async def scrape_website(url, browser):
    scraper = Scraper()
    text = await scraper.scrape(url, browser)
    return text
