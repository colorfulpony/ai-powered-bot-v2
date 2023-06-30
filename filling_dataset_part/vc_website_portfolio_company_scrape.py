import time
import traceback

from bs4 import BeautifulSoup


async def scrap_portfolio_website(url: str, browser) -> str:
    """
    Scrapes the content of a vc's portfolio startup website.

    Parameters:
        url (str): The URL of the portfolio website to scrape.
        browser: The browser object to use for scraping (playwright).

    Returns:
        str: The scraped text if successful, or an empty string if an error occurs.
    """
    text = ""
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0"

    try:
        page = await browser.new_page()
        page.set_default_navigation_timeout(40000)
        await page.set_extra_http_headers({"User-Agent": user_agent})

        await page.goto(url)
        time.sleep(3)
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        await page.close()
    except Exception as e:
        await page.close()
        print(e)
        traceback.print_exc()
        return ""

    await page.close()
    return text
