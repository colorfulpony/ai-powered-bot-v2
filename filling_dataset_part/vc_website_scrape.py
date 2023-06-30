import traceback

from bs4 import BeautifulSoup
import urllib.parse


class Scraper:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0"

    async def scrape(self, url: str, browser) -> str:
        """
        Scrape a website and return its text content.

        Parameters:
            url (str): The URL of the website to scrape.
            browser: The browser object to use for scraping (puppeteer or similar).

        Returns:
            str: The scraped text if successful, or an empty string if an error occurs.
        """
        visited_urls = set()
        try:
            page = await browser.new_page()
            page.set_default_navigation_timeout(40000)
            await page.set_extra_http_headers({"User-Agent": self.user_agent})
            text = await self.scrape_main(page, url, visited_urls)
            await page.close()
        except Exception as e:
            await page.close()
            print(e)
            traceback.print_exc()
            return ""

        await page.close()
        return text

    @staticmethod
    async def extract_text(page, url: str) -> str:
        """
        Extract the text content from a webpage.

        Parameters:
            page: The page object representing the webpage.
            url (str): The URL of the webpage.

        Returns:
            str: The extracted text content if successful, or an empty string if an error occurs.
        """
        try:
            await page.goto(url)
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            return text
        except Exception as e:
            print(e)
            traceback.print_exc()
            return ""

    async def scrape_main(self, page, start_url, visited_urls):
        """
        Scrap main(landing) page that recursively scrapes the website and its subpages.

        Parameters:
            page: The page object representing the webpage.
            start_url (str): The starting URL of the website.
            visited_urls (set): Set of visited URLs to avoid duplicate scraping.

        Returns:
            str: The concatenated text content of the website and its subpages.
        """
        text = ""
        try:
            visited_urls.add(start_url)
            text += await self.extract_text(page, start_url)
            await page.goto(start_url)
            soup = BeautifulSoup(await page.content(), 'html.parser')

            # Filter all link to find only subpages of vc's website
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

                visited_urls.add(abs_url)
                text += await self.scrape_subpages(page, abs_url)

            return text
        except Exception as e:
            print(e)
            traceback.print_exc()
            return ""

    @staticmethod
    async def scrape_subpages(page, url: str) -> str:
        """
        Scrape a subpage of a website and return its text content.

        Parameters:
            page: The page object representing the webpage.
            url (str): The URL of the subpage.

        Returns:
            str: The scraped text if successful, or an empty string if an error occurs.
        """
        try:
            text = ""
            text += await Scraper.extract_text(page, url)
            return text
        except Exception as e:
            print(e)
            traceback.print_exc()
            return ""


async def scrape_website(url, browser):
    """
    Scrape a website and return its text content.

    Parameters:
        url (str): The URL of the website to scrape.
        browser: The browser object to use for scraping (puppeteer or similar).

    Returns:
        str: The scraped text if successful, or an empty string if an error occurs.
    """
    try:
        scraper = Scraper()
        text = await scraper.scrape(url, browser)
        return text
    except Exception as e:
        print(e)
        traceback.print_exc()
        return ""
