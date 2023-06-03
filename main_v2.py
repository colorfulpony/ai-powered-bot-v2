from urllib.parse import urlparse
from vc_website_portfolio_company_scrape_v2 import scrap_portfolio_website
from clean_text_after_scrape import clean_text
from vc_website_scrape_v2 import scrape_website
from vc_website_portfolio_links_v2 import get_portfolio_links
from get_gpt_response_via_text import gpt_info_via_text
from get_gpt_response_via_text_for_portfolio_website_solution import gpt_info_via_text as gpt_portfolio_startup_solution
import questions as constants
import prompts as INPUTS
from gpt_repeat_answer_2_times import repeat_gpt_answer_2_time
from get_info_from_sheets import get_data_from_google_sheets
from playwright.async_api import async_playwright
import asyncio
import time
import traceback


async def get_info_about_vc(vc_name, url, browser) -> tuple:
    try:
        start_scrape_text = time.time()
        raw_text = await scrape_website(url, browser)
        end_scrape_text = time.time()
        print(f'Execution time of scraping vc website: {end_scrape_text - start_scrape_text}')
        cleaned_text = clean_text(raw_text)
        cleaned_text = f"Info about venture capital with name {vc_name}. \n{cleaned_text}"


        industries_stages_start_scrape_text = time.time()

        industries_start_scrape_text = time.time()
        industries = await gpt_info_via_text(cleaned_text, INPUTS.INDUSTRIES_INPUT)
        industries_end_scrape_text = time.time()
        print(f'Industries exec time: {industries_end_scrape_text - industries_start_scrape_text}')

        stages_start_scrape_text = time.time()
        stages = await gpt_info_via_text(cleaned_text, INPUTS.STAGES_INPUT)
        stages_end_scrape_text = time.time()
        print(f'Stages exec time: {stages_end_scrape_text - stages_start_scrape_text}')

        industries_stages_end_scrape_text = time.time()
        print(f'Industries + stages execution full time: {industries_stages_end_scrape_text - industries_stages_start_scrape_text}')

        return industries, stages
    except Exception as error:
        print(error)
        traceback.print_exc()


async def process_startup(portfolio_startup_link, browser):
    try:
        text_from_startup_website = await scrap_portfolio_website(portfolio_startup_link, browser)
        if text_from_startup_website == "":
            return None

        domain_name = urlparse(portfolio_startup_link).netloc
        startup_name = domain_name.split('.')[0] if domain_name.count('.') == 1 else domain_name.split('.')[1]
        text_from_startup_website = f"Name of the startup is {startup_name}.\n{text_from_startup_website}"
        start_startup_solution = time.time()
        startup_solution = await gpt_portfolio_startup_solution(text_from_startup_website, constants.SOLUTION_QUESTION)
        end_startup_solution = time.time()
        print(
            f'Execution time of getting full info about all startups from vc portfolio: {end_startup_solution - start_startup_solution}')

        if any(keyword in startup_solution for keyword in ("I don't know", "This document does not", "context does not provide")):
            return None

        return startup_name, portfolio_startup_link, startup_solution
    except Exception as error:
        print(error)
        traceback.print_exc()

async def get_info_about_vc_portfolio_startups(portfolio_url, max_portfolios=10, browser=None):
    try:
        full_start_startup_solution = time.time()

        startups_result_info = []

        portfolio_startups_links = await get_portfolio_links(portfolio_url, browser)
        if len(portfolio_startups_links) >= 10:
            ten_portfolio_startups_links = portfolio_startups_links[:10]
        else:
            ten_portfolio_startups_links = portfolio_startups_links

        tasks = []
        for link in ten_portfolio_startups_links:
            task = asyncio.create_task(process_startup(link, browser))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        startups_result_info = [result for result in results if result is not None]
        full_end_startup_solution = time.time()
        print(
            f'Full exec of startups: {full_end_startup_solution - full_start_startup_solution}')

        return startups_result_info
    except Exception as error:
        print(error)
        traceback.print_exc()


async def process_vc_data(vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name, analyst_email,
                          vc_stages, vc_industries, browser) -> tuple:
    start_vc_portfolio = time.time()
    portfolio_startups = await get_info_about_vc_portfolio_startups(vc_portfolio_url, browser=browser)
    print(portfolio_startups)
    end_vc_portfolio = time.time()
    print(f'Execution time of getting startup solution: {end_vc_portfolio - start_vc_portfolio}')

    start_vc_industries = time.time()
    if vc_stages == "-" or vc_industries == "-":
        industries, stages = await get_info_about_vc(vc_name, vc_website_url, browser)
        vc_industries = f"{vc_industries}, {industries}" if vc_industries != "-" else industries
        vc_stages = f"{vc_stages}, {stages}" if vc_stages != "-" else stages
    end_vc_industries = time.time()
    print(f'Execution time of getting full info about vc industries and stages: {end_vc_industries - start_vc_industries}')

    return vc_name, vc_website_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, portfolio_startups


async def main():
    start = time.time()
    print("AI Powered Chat")

    async with async_playwright() as p:
        num_browsers = 5  # Number of browser instances to launch
        browsers = await asyncio.gather(*[p.chromium.launch(headless=True) for _ in range(num_browsers)])

        data_from_sheets = get_data_from_google_sheets("A2:H2")

        tasks = []
        semaphore = asyncio.Semaphore(num_browsers)  # Limit concurrent tasks to the number of browser instances
        for vc_data in data_from_sheets:
            vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries = vc_data

            async def process_vc():
                async with semaphore:
                    return await process_vc_data(vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name,
                                                analyst_email, vc_stages, vc_industries, browsers.pop())

            task = asyncio.create_task(process_vc())
            tasks.append(task)

        processed_data = await asyncio.gather(*tasks)
        print(processed_data)

        await asyncio.gather(*[browser.close() for browser in browsers])

    end = time.time()
    print(f'Full execution time: {end - start}')


if __name__ == "__main__":
    asyncio.run(main())
