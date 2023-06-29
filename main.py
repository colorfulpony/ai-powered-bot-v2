import asyncio
import time
import traceback
from urllib.parse import urlparse
from playwright.async_api import async_playwright

from vc_website_portfolio_company_scrape import scrap_portfolio_website
from clean_text_after_scrape import clean_text
from vc_website_scrape import scrape_website
from vc_website_portfolio_links import get_portfolio_links
from get_gpt_response_via_text import gpt_info_via_text
from get_gpt_response_via_text_for_portfolio_startup import gpt_info_via_text as gpt_portfolio_startup_solution
import questions as constants
import prompts as INPUTS
from insert_into_sheets_v2 import insert_data_into_google_sheets
from get_info_from_sheets import get_data_from_google_sheets


async def get_info_about_vc(vc_name, url, browser) -> tuple:
    try:
        raw_text = await scrape_website(url, browser)
        if raw_text != "":
            cleaned_text = clean_text(raw_text)
            cleaned_text = f"Info about venture capital with name {vc_name}. \n{cleaned_text}"

            industries_task = asyncio.create_task(gpt_info_via_text(cleaned_text, INPUTS.INDUSTRIES_INPUT))

            stages_task = asyncio.create_task(gpt_info_via_text(cleaned_text, INPUTS.STAGES_INPUT))

            await asyncio.gather(industries_task, stages_task)

            industries = industries_task.result()
            if industries.startswith("I don't know") or "does not provide" in industries or "without further information" in industries:
                industries = None

            stages = stages_task.result()
            if stages.startswith("I don't know") or "does not provide" in stages or "without further information" in stages:
                stages = None

            return industries, stages
        else:
            return None, None
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None, None


async def process_startup(portfolio_startup_link, browser):
    try:
        text_from_startup_website = await scrap_portfolio_website(portfolio_startup_link, browser)

        if text_from_startup_website == "":
            return None

        domain_name = urlparse(portfolio_startup_link).netloc
        startup_name = domain_name.split('.')[0] if domain_name.count('.') == 1 else domain_name.split('.')[1]
        startup_solution = await gpt_portfolio_startup_solution(text_from_startup_website, constants.SOLUTION_QUESTION)
        startup_industry = await gpt_portfolio_startup_solution(text_from_startup_website, constants.INDUSTRY_QUESTION)

        if any(keyword in startup_solution for keyword in ("I don't know", "This document does not", "context does not provide")):
            startup_solution = None

        if any(keyword in startup_industry for keyword in ("I don't know", "This document does not", "context does not provide")):
            startup_industry = None

        return startup_name, portfolio_startup_link, startup_solution, startup_industry
    except Exception as e:
        print(e)
        traceback.print_exc()


async def get_info_about_vc_portfolio_startups(portfolio_url, browser=None):
    try:
        startups_result_info = []
        start_startup_links = time.time()
        portfolio_startups_links = await get_portfolio_links(portfolio_url, browser)
        if portfolio_startups_links is None:
            return None
        end_startup_links = time.time()
        print(f'Full exec startup links: {end_startup_links - start_startup_links}')

        tasks = []
        for link in portfolio_startups_links:
            task = asyncio.create_task(process_startup(link, browser))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        startups_result_info = [result for result in results if result is not None]

        return startups_result_info  # Return the first 10 startups (or fewer)

    except Exception as error:
        print(error)
        traceback.print_exc()


async def process_vc_data(
        vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url,
        analyst_name, analyst_email, vc_stages, vc_industries, browser
) -> tuple:
    try:
        portfolio_startups = await get_info_about_vc_portfolio_startups(vc_portfolio_url, browser=browser)

        industries, stages = await get_info_about_vc(vc_name, vc_website_url, browser)
        if industries is not None:
            vc_industries = vc_industries + ", " + industries
        if stages is not None:
            vc_stages = vc_stages + ", " + stages

        for portfolio_startup in portfolio_startups:
            if portfolio_startup[3] is not None:
                vc_industries = vc_industries + ", " + portfolio_startup[3]

        return vc_name, vc_website_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, portfolio_startups
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None, None, None, None, None, None, None, None


async def process_vc(semaphore, vc_data, browser_pool):
    try:
        async with semaphore:
            vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries = vc_data
            browser = await browser_pool.get()
            try:
                processed_vc_data = await process_vc_data(
                    vc_name, vc_website_url, vc_portfolio_url,
                    vc_linkedin_url, analyst_name, analyst_email,
                    vc_stages, vc_industries, browser
                )

                if processed_vc_data == (None, None, None, None, None, None, None, None):
                    raise ValueError("There is no processed VC data. Stopping execution")

                return processed_vc_data
            finally:
                await browser_pool.put(browser)
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None


async def change_data_format(data):
    rows = []
    row_data = []
    vc_name = data[0]
    vc_website = data[1]
    vc_linkedin = data[2]
    analyst_name = data[3]
    analyst_email = data[4]
    vc_stage = data[5]
    vc_industry = data[6]

    # Flatten nested items and insert as separate rows
    if data[7] is not None and len(data[7]) != 0:
        for nested_item in data[7]:
            startup_name = nested_item[0]
            startup_website = nested_item[1]
            startup_solution = nested_item[2]

            # Insert data as a row
            row_data = [
                vc_name, vc_website, vc_linkedin, analyst_name,
                analyst_email, vc_stage, vc_industry,
                startup_name, startup_website, startup_solution
            ]
            rows.append(row_data)
    else:
        startup_name = "-"
        startup_website = "-"
        startup_solution = "-"

        row_data = [
            vc_name, vc_website, vc_linkedin, analyst_name,
            analyst_email, vc_stage, vc_industry,
            startup_name, startup_website, startup_solution
        ]

        rows.append(row_data)
    return rows


async def main(google_sheets_range):
    try:
        google_sheets_rows = []
        start = time.time()
        print("AI Powered Chat")
        data_from_sheets = get_data_from_google_sheets(google_sheets_range)
        if data_from_sheets is None:
            raise ValueError("Data from Google Sheets is None. Stopping execution.")
        for vc_data in data_from_sheets:
            if vc_data[2] == "/" or vc_data[2] == "" or vc_data[4] == "/" or vc_data[4] == "" or vc_data[5] == "/" or vc_data[5] == "":
                continue
            else:
                async with async_playwright() as p:
                    num_browsers = 3  # Number of browser instances to launch
                    browsers = await asyncio.gather(*[p.chromium.launch(headless=True) for _ in range(num_browsers)])
                    browser_pool = asyncio.Queue()
                    for browser in browsers:
                        await browser_pool.put(browser)

                    tasks = []
                    semaphore = asyncio.Semaphore(num_browsers)  # Limit concurrent tasks to the number of browser instances
                    for vc_data in data_from_sheets:
                        if vc_data[2] == "/" or vc_data[2] == "" or vc_data[4] == "/" or vc_data[4] == "" or vc_data[5] == "/" or vc_data[5] == "":
                            continue
                        task = asyncio.create_task(process_vc(semaphore, vc_data, browser_pool))
                        tasks.append(task)

                    processed_data = await asyncio.gather(*tasks)
                    print('PROCESSED DATA')
                    print(processed_data)
                    print("Processed Venture Capital Data:")
                    print("-" * 50)
                    for data in processed_data:
                        rows = []
                        vc_name, vc_website_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, portfolio_startups = data
                        rows = await change_data_format(data)
                        for row in rows:
                            google_sheets_rows.append(row)
                        print(f"VC Name: {vc_name}")
                        print(f"Website URL: {vc_website_url}")
                        print(f"LinkedIn URL: {vc_linkedin_url}")
                        print(f"Analyst Name: {analyst_name}")
                        print(f"Analyst Email: {analyst_email}")
                        print(f"Stages: {vc_stages}")
                        print(f"Industries: {vc_industries}")
                        print("Portfolio Startups:")
                        if portfolio_startups:
                            for startup_name, startup_url, startup_solution, _ in portfolio_startups:
                                print(f"    - Startup Name: {startup_name}")
                                print(f"      Startup URL: {startup_url}")
                                print(f"      Solution: {startup_solution}")
                        else:
                            print("    No portfolio startups found.")
                        print("-" * 50)

                    print("GOOGLE SHEETS ROWS")
                    print(google_sheets_rows)
                    await insert_data_into_google_sheets(google_sheets_rows)
                    await asyncio.gather(*[browser.close() for browser in browsers])

                end = time.time()
                print(f'Full execution time: {end - start}')
    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    for i in range(2, 20):
        print(i)
        asyncio.run(main(f'A{i}:H{i}'))