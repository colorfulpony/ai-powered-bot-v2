import asyncio
import time
import traceback
from urllib.parse import urlparse
from playwright.async_api import async_playwright

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
            stages = stages_task.result()

            return industries, stages
        else:
            return None, None
    except Exception as error:
        # print(error)
        traceback.print_exc()


async def process_startup(portfolio_startup_link, browser):
    try:
        text_from_startup_website = await scrap_portfolio_website(portfolio_startup_link, browser)

        if text_from_startup_website == "":
            return None, None, None

        domain_name = urlparse(portfolio_startup_link).netloc
        startup_name = domain_name.split('.')[0] if domain_name.count('.') == 1 else domain_name.split('.')[1]
        text_from_startup_website = f"Name of the startup is {startup_name}.\n{text_from_startup_website}"
        startup_solution = await gpt_portfolio_startup_solution(text_from_startup_website, constants.SOLUTION_QUESTION)

        if any(keyword in startup_solution for keyword in ("I don't know", "This document does not", "context does not provide")):
            return None, None, None

        return startup_name, portfolio_startup_link, startup_solution
    except Exception as error:
        # print(error)
        traceback.print_exc()


async def get_info_about_vc_portfolio_startups(portfolio_url, browser=None):
    try:
        startups_result_info = []
        start_startup_links = time.time()
        portfolio_startups_links = await get_portfolio_links(portfolio_url, browser)
        end_startup_links = time.time()
        print(f'Full exec startup links: {end_startup_links - start_startup_links}')

        tasks = []
        for link in portfolio_startups_links:
            task = asyncio.create_task(process_startup(link, browser))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        startups_result_info = [result for result in results if result != (None, None, None)]

        # Check if the number of startups is less than 10 and there are additional links available
        # while len(startups_result_info) < 10 and len(portfolio_startups_links) > len(tasks):
        #     remaining_links = portfolio_startups_links[len(tasks):]
        #     additional_tasks = []
        #     for link in remaining_links:
        #         task = asyncio.create_task(process_startup(link, browser))
        #         additional_tasks.append(task)
        #
        #     additional_results = await asyncio.gather(*additional_tasks)
        #     additional_startups_info = [result for result in additional_results if result is not None]
        #     startups_result_info.extend(additional_startups_info)
        #     tasks.extend(additional_tasks)

        return startups_result_info[:10]  # Return the first 10 startups (or fewer)

    except Exception as error:
        print(error)
        traceback.print_exc()



async def process_vc_data(vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name, analyst_email,
                          vc_stages, vc_industries, browser) -> tuple:
    start_vc_portfolio = time.time()
    portfolio_startups = await get_info_about_vc_portfolio_startups(vc_portfolio_url, browser=browser)
    # print(portfolio_startups)
    end_vc_portfolio = time.time()
    # print(f'Execution time of getting startup solution: {end_vc_portfolio - start_vc_portfolio}')

    start_vc_industries = time.time()
    if vc_stages == "-" or vc_industries == "-":
        industries, stages = await get_info_about_vc(vc_name, vc_website_url, browser)
        vc_industries = f"{vc_industries}, {industries}" if vc_industries != "-" else industries
        vc_stages = f"{vc_stages}, {stages}" if vc_stages != "-" else stages
    end_vc_industries = time.time()
    # print(f'Execution time of getting full info about vc industries and stages: {end_vc_industries - start_vc_industries}')

    return vc_name, vc_website_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, portfolio_startups


async def process_vc(semaphore, vc_data, browser_pool):
    async with semaphore:
        vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries = vc_data
        browser = await browser_pool.get()
        try:
            return await process_vc_data(vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name,
                                        analyst_email, vc_stages, vc_industries, browser)
        finally:
            await browser_pool.put(browser)


async def main():
    start = time.time()
    print("AI Powered Chat")

    async with async_playwright() as p:
        num_browsers = 5  # Number of browser instances to launch
        browsers = await asyncio.gather(*[p.chromium.launch(headless=True) for _ in range(num_browsers)])
        browser_pool = asyncio.Queue()
        for browser in browsers:
            await browser_pool.put(browser)

        data_from_sheets = get_data_from_google_sheets("A2:H10")
        print(data_from_sheets)

        tasks = []
        semaphore = asyncio.Semaphore(num_browsers)  # Limit concurrent tasks to the number of browser instances
        for vc_data in data_from_sheets:
            task = asyncio.create_task(process_vc(semaphore, vc_data, browser_pool))
            tasks.append(task)

        processed_data = await asyncio.gather(*tasks)
        print("Processed Venture Capital Data:")
        print("-" * 50)
        for data in processed_data:
            vc_name, vc_website_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, portfolio_startups = data

            print(f"VC Name: {vc_name}")
            print(f"Website URL: {vc_website_url}")
            print(f"LinkedIn URL: {vc_linkedin_url}")
            print(f"Analyst Name: {analyst_name}")
            print(f"Analyst Email: {analyst_email}")
            print(f"Stages: {vc_stages}")
            print(f"Industries: {vc_industries}")
            print("Portfolio Startups:")
            if portfolio_startups:
                for startup_name, startup_url, startup_solution in portfolio_startups:
                    print(f"    - Startup Name: {startup_name}")
                    print(f"      Startup URL: {startup_url}")
                    print(f"      Solution: {startup_solution}")
            else:
                print("    No portfolio startups found.")
            print("-" * 50)

        await asyncio.gather(*[browser.close() for browser in browsers])

    end = time.time()
    print(f'Full execution time: {end - start}')


if __name__ == "__main__":
    asyncio.run(main())
