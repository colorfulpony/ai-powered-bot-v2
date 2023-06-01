from urllib.parse import urlparse
from vc_website_portfolio_company_scrape_v2 import scrap_portfolio_website
from clean_text_after_scrape import clean_text
from vc_website_portfolio_links_v2 import get_portfolio_links
from get_gpt_response_via_text import gpt_info_via_text
from get_gpt_response_via_text_for_portfolio_website_solution import gpt_info_via_text as gpt_portfolio_startup_solution
from insert_into_google_sheets import insert_data_into_google_sheets
from vc_website_scrape_v2 import scrape_website
import questions as constants
import prompts as INPUTS
from gpt_repeat_answer_3_times import repeat_gpt_answer_3_time
from get_info_from_sheets import get_data_from_google_sheets
from playwright.sync_api import sync_playwright
from multiprocessing import Pool
from functools import partial
from get_all_subpages_links_of_vc import get_vc_subpages_links


def get_info_about_vc(vc_name, url, browser) -> tuple:
    try:
        links = get_vc_subpages_links(url, browser)
        raw_text = scrape_website(url, browser)
        cleaned_text = clean_text(raw_text)
        cleaned_text = f"Info about venture capital with name {vc_name}. \n{cleaned_text}"

        industries = repeat_gpt_answer_3_time(gpt_info_via_text, cleaned_text, INPUTS.INDUSTRIES_INPUT)
        stages = repeat_gpt_answer_3_time(gpt_info_via_text, cleaned_text, INPUTS.STAGES_INPUT)

        if any(keyword in industries for keyword in ("I don't know", "This document does not", "context does not provide")):
            industries = "-"
        if any(keyword in stages for keyword in ("I don't know", "This document does not", "context does not provide")):
            stages = "-"

        return industries, stages
    except Exception as error:
        print(error)


def get_info_about_vc_portfolio_startups(portfolio_url, max_portfolios=10, browser=None) -> list:
    try:
        startups_result_info = []

        portfolio_startups_links = get_portfolio_links(portfolio_url, browser)

        for portfolio_startup_link in portfolio_startups_links[:max_portfolios]:
            text_from_startup_website = scrap_portfolio_website(portfolio_startup_link, browser)
            if text_from_startup_website == "-":
                continue

            domain_name = urlparse(portfolio_startup_link).netloc
            startup_name = domain_name.split('.')[0] if domain_name.count('.') == 1 else domain_name.split('.')[1]
            text_from_startup_website = f"Name of the startup is {startup_name}.\n{text_from_startup_website}"

            startup_solution = gpt_portfolio_startup_solution(text_from_startup_website, constants.SOLUTION_QUESTION)

            if any(keyword in startup_solution for keyword in ("I don't know", "This document does not", "context does not provide")):
                continue

            startups_result_info.append((startup_name, portfolio_startup_link, startup_solution))

        return startups_result_info
    except Exception as error:
        print(error)


def process_vc_data(vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, browser) -> tuple:
    portfolio_startups = get_info_about_vc_portfolio_startups(vc_portfolio_url, browser=browser)
    if vc_stages == "-" or vc_industries == "-":
        industries, stages = get_info_about_vc(vc_name, vc_website_url, browser)
        vc_industries = f"{vc_industries}, {industries}" if vc_industries else industries
        vc_stages = f"{vc_stages}, {stages}" if vc_stages else stages

    return vc_name, vc_website_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, portfolio_startups


if __name__ == "__main__":
    print("AI Powered Chat")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        data_from_sheets = get_data_from_google_sheets("A2:H3")

        for vc_data in data_from_sheets:
            vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries = vc_data
            processed_data = process_vc_data(vc_name, vc_website_url, vc_portfolio_url, vc_linkedin_url, analyst_name, analyst_email, vc_stages, vc_industries, browser)
            insert_data_into_google_sheets(*processed_data)
            print(processed_data[-1])  # Print portfolio startups

        browser.close()
