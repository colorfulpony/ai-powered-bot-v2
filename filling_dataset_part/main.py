import asyncio
import os
import time
import traceback
from urllib.parse import urlparse
from dotenv import load_dotenv
from pathlib import Path

import openai
from playwright.async_api import async_playwright

from filling_dataset_part.vc_website_portfolio_company_scrape import scrap_portfolio_website
from filling_dataset_part.clean_text_after_scrape import clean_text
from filling_dataset_part.vc_website_scrape import scrape_website
from filling_dataset_part.vc_website_portfolio_links import get_portfolio_links
from filling_dataset_part.get_gpt_response_via_text import gpt_info_via_text
from filling_dataset_part.get_gpt_response_via_text_for_portfolio_startup import gpt_info_via_text as gpt_portfolio_startup_solution
from constants import prompts as INPUTS, questions as constants
from filling_dataset_part.insert_into_sheets import insert_data_into_google_sheets
from filling_dataset_part.get_info_from_sheets import get_data_from_google_sheets


dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


# Retrieve information about the venture capital from a given website
async def get_info_about_vc(vc_name, url, browser) -> str:
    """
    Retrieve information about the venture capital from a given website.

    Parameters:
        vc_name (str): The name of the venture capital.
        url (str): The URL of the venture capital's website.
        browser: The browser object to use for scraping (puppeteer or similar).

    Returns:
        str: A string containing information about the investment stages.
    """
    try:
        # Scrape VC website to get plain text
        raw_text = await scrape_website(url, browser)
        if raw_text != "":
            # Clean from duplicates text from VC website
            cleaned_text = clean_text(raw_text)
            cleaned_text = f"Info about venture capital with name {vc_name}. \n{cleaned_text}"

            # Get stages in which VC invest based on VC's website text
            stages_task = asyncio.create_task(gpt_info_via_text(cleaned_text, INPUTS.STAGES_INPUT))

            await asyncio.gather(stages_task)

            stages = stages_task.result()

            # Check if we got correct answer from GPT
            if stages.startswith("I don't know") or "does not provide" in stages or "without further information" in stages:
                stages = None

            return stages
        else:
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None


# Process a startup from the venture capital's portfolio
async def process_startup(portfolio_startup_link, browser):
    """
    Process a startup from the venture capital's portfolio.

    Parameters:
        portfolio_startup_link (str): The URL of the startup's website.
        browser: The browser object to use for scraping (puppeteer or similar).

    Returns:
        tuple: A tuple containing information about the startup.
    """
    try:
        # Get plain text from startup's website
        text_from_startup_website = await scrap_portfolio_website(portfolio_startup_link, browser)

        if text_from_startup_website == "":
            return None

        # Get name of startup based on it's domain
        domain_name = urlparse(portfolio_startup_link).netloc
        startup_name = domain_name.split('.')[0] if domain_name.count('.') == 1 else domain_name.split('.')[1]

        # Get problem solution that this startup provides
        startup_solution = await gpt_portfolio_startup_solution(text_from_startup_website, constants.SOLUTION_QUESTION)

        # Get industry(s) in which this startup works
        startup_industry = await gpt_portfolio_startup_solution(text_from_startup_website, constants.INDUSTRY_QUESTION)

        return startup_name, portfolio_startup_link, startup_solution, startup_industry
    except Exception as e:
        print(e)
        traceback.print_exc()


# Retrieve information about startups in the venture capital's portfolio
async def get_info_about_vc_portfolio_startups(portfolio_url, browser=None):
    """
    Retrieve information about startups in the venture capital's portfolio.

    Parameters:
        portfolio_url (str): The URL of the venture capital's portfolio.
        browser: The browser object to use for scraping (puppeteer or similar).

    Returns:
        list: A list of tuples containing information about the startups in the portfolio.
    """
    try:
        startups_result_info = []
        start_startup_links = time.time()

        # Find all links to startup's website in which this VC has invested before
        portfolio_startups_links = await get_portfolio_links(portfolio_url, browser)
        if portfolio_startups_links is None:
            return None

        end_startup_links = time.time()

        print(f'Full exec startup links: {end_startup_links - start_startup_links}')

        tasks = []
        for link in portfolio_startups_links[:10]:
            task = asyncio.create_task(process_startup(link, browser))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        # Make list of startups links
        startups_result_info = [result for result in results if result is not None]

        return startups_result_info

    except Exception as error:
        print(error)
        traceback.print_exc()


# Process the data of a venture capital
async def process_vc_data(
        vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url,
        analyst_name, analyst_email, vc_stages, vc_industries, browser
) -> tuple:
    """
        Process the data of a venture capital.

        Parameters:
            vc_name (str): The name of the venture capital.
            vc_website_url (str): The URL of the venture capital's website.
            vc_portfolio_url (str): The URL of the venture capital's portfolio.
            vc_linkedin_url (str): The URL of the venture capital's LinkedIn page.
            analyst_name (str): The name of the analyst.
            analyst_email (str): The email of the analyst.
            vc_stages (str): The stages in which the venture capital invests.
            vc_industries (str): The industries in which the venture capital invests.
            browser: The browser object to use for scraping (puppeteer or similar).

        Returns:
            tuple: A tuple containing processed information about the venture capital.
    """
    try:
        # Get info about portfolio startups
        portfolio_startups = await get_info_about_vc_portfolio_startups(vc_portfolio_url, browser=browser)

        # Get stages in which VC invest
        stages = await get_info_about_vc(vc_name, vc_website_url, browser)

        if stages is not None:
            vc_stages = vc_stages + ", " + stages

        # Add industries of startup to `vc_industries` that indicated in which industries invest VC
        if portfolio_startups:
            for portfolio_startup in portfolio_startups:
                if portfolio_startup[3] is not None:
                    vc_industries = vc_industries + ", " + portfolio_startup[3]

        return vc_name, vc_website_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, portfolio_startups
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None, None, None, None, None, None, None, None


# Process the venture capital data
async def process_vc(semaphore, vc_data, browser_pool):
    """
        Process the venture capital data.

        Parameters:
            semaphore: The semaphore object for limiting concurrent tasks.
            vc_data: The data of the venture capital to process.
            browser_pool: The queue of browser instances to use for scraping.

        Returns:
            tuple: A tuple containing processed information about the venture capital.
    """
    try:
        async with semaphore:
            vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries = vc_data
            browser = await browser_pool.get()
            try:
                # Process all vc information we need for final output
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


# Change the data format to insert into Google Sheets
async def change_data_format(data):
    """
        Change the data format to insert into Google Sheets.

        Parameters:
            data: The processed data to be formatted.

        Returns:
            list: A list of rows in the desired format for Google Sheets insertion.
    """
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


# Main function to execute the program
async def main(google_sheets_range):
    """
    Main function to execute the program.

    Parameters:
        google_sheets_range (str): The range of Google Sheets to fetch data from.

    Returns:
        None
    """
    try:
        google_sheets_rows = []
        start = time.time()

        print("AI Powered Chat")

        # Get information from Google Sheet
        data_from_sheets = get_data_from_google_sheets(google_sheets_range)

        # Check if data from VC is not None
        if data_from_sheets is None:
            raise ValueError("Data from Google Sheets is None. Stopping execution.")

        # Iterate through each row from Google Sheets
        for vc_data in data_from_sheets:
            # Check if `Company Portfolio Url`, `Investor Full Name` ,`Investor Email` aren't empty. If empty - we skip this row
            if vc_data[2] == "/" or vc_data[2] == "" or vc_data[4] == "/" or vc_data[4] == "" or vc_data[5] == "/" or vc_data[5] == "":
                continue
            else:
                async with async_playwright() as p:
                    # Create browser pool for async work
                    num_browsers = 3  # Number of browser instances to launch
                    browsers = await asyncio.gather(*[p.chromium.launch(headless=True) for _ in range(num_browsers)])
                    browser_pool = asyncio.Queue()
                    for browser in browsers:
                        await browser_pool.put(browser)

                    tasks = []
                    semaphore = asyncio.Semaphore(num_browsers)  # Limit concurrent tasks to the number of browser instances

                    # Make tasks for async work
                    task = asyncio.create_task(process_vc(semaphore, vc_data, browser_pool))
                    tasks.append(task)

                    # Process data
                    processed_data = await asyncio.gather(*tasks)

                    # Print output
                    print('PROCESSED DATA')
                    print(processed_data)
                    print("Processed Venture Capital Data:")
                    print("-" * 50)

                    # Insert data into final Google Sheets
                    for data in processed_data:
                        rows = []
                        vc_name, vc_website_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, portfolio_startups = data

                        # Change data format for Google Sheets
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

                    # Add data to final Google Sheets
                    await insert_data_into_google_sheets(google_sheets_rows)
                    await asyncio.gather(*[browser.close() for browser in browsers])

                end = time.time()
                print(f'Full execution time: {end - start}')
    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    for i in range(1941, 2000):
        print(i)
        asyncio.run(main(f'A{i}:H{i}'))