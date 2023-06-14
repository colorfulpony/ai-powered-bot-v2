import time
import traceback

import aiohttp
from bs4 import BeautifulSoup


async def get_status_code(url: str) -> int:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status
    except aiohttp.ClientError as e:
        print(e)
        traceback.print_exc()
        return 0


async def scrap_portfolio_website(url: str, browser) -> str:
    text = ""
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0"

    try:
        page = await browser.new_page()
        page.set_default_navigation_timeout(20000)
        await page.set_extra_http_headers({"User-Agent": user_agent})

        # status_code = await get_status_code(url)
        # if 200 <= status_code < 300:
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
