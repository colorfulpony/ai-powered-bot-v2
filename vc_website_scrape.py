import urllib.parse
from bs4 import BeautifulSoup
import logging
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

logging.basicConfig(filename='scraping.log', level=logging.INFO)

class Scraper:
    def scrape(self, url: str) -> str:
        text = ""
        visited_urls = set()
        try:
            text = self.scrape_main(url, visited_urls)
        except Exception as e:
            logging.error(f"Error launching browser while main scraping: {e}")
        return text

    @staticmethod
    def extract_text(url: str) -> str:
        try:
            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('--headless')
            options.add_argument("--user-data-dir=C:/Users/flexy/AppData/Local/Google/Chrome/User Data/Default")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0")

            service = Service('C:/Users/flexy/PycharmProjects/pythonProject2/chromedriver.exe')
            service.start()
            driver = webdriver.Remote(service.service_url, options=options)
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            logging.info(f"Visited url:{url}")
            return text
        except Exception as e:
            logging.error(f"Error requesting while main scraping {url}: {e}")
            return ""
        finally:
            driver.quit()

    def scrape_main(self, start_url, visited_urls):
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--headless')
        options.add_argument("--user-data-dir=C:/Users/flexy/AppData/Local/Google/Chrome/User Data/Default")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0")

        service = Service('C:/Users/flexy/PycharmProjects/pythonProject2/chromedriver.exe')
        service.start()
        driver = webdriver.Remote(service.service_url, options=options)
        text = ""
        visited_urls.add(start_url)
        text += self.extract_text(start_url)
        driver.get(start_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href or href.startswith("mailto:"):
                continue
            abs_url = urllib.parse.urljoin(start_url, href)
            logging.info(f"BEFORE ABS url: {abs_url}")

            if abs_url.startswith("http://"):
                abs_url = abs_url.replace("http://", "https://")

            if abs_url.startswith('/') or abs_url.startswith("#"):
                abs_url = urllib.parse.urljoin(start_url, abs_url)

            logging.info(f"ABS url: {abs_url}")
            if not abs_url.startswith(start_url) or not abs_url.startswith('https'):
                continue
            if abs_url in visited_urls:
                continue
            try:
                visited_urls.add(abs_url)
                text += self.scrape_subpages(abs_url)
            except Exception as e:
                logging.error(f"Error while main scraping {abs_url}: {e}")
        return text

    @staticmethod
    def scrape_subpages(url: str) -> str:
        text = ""
        text += Scraper.extract_text(url)
        return text


def scrape_website(url):
    scraper = Scraper()
    text = scraper.scrape(url)
    return text
