import logging
from website_scrapping.vc_website_portfolio_company_scrape import scrap_portfolio_website
from clean_text_after_scrapping.clean_text_after_scrape import clean_text
from website_scrapping.vc_website_portfolio_links import get_portfolio_links
from gpt_main_packages.get_gpt_response_via_text import gpt_info_via_text

import gpt_constants.questions as constants
import gpt_constants.response_schemas as schemas

from gpt_stuff.main import repeat_gpt_answer_5_time

logging.basicConfig(filename='scraping.log', level=logging.INFO)


def get_info_about_vc(url):
    try:
        industries = repeat_gpt_answer_5_time(url, schemas.INDUSTRIES_RESPONSE_SCHEMA, constants.INDUSTRIES_QUESTION)
        stages = repeat_gpt_answer_5_time(url, schemas.STAGES_RESPONSE_SCHEMA, constants.STAGES_QUESTION)

        logging.info(f"Processed URL: {url}")

        return industries, stages
    except Exception as error:
        logging.error(f"Error processing URL {url}: {error}")


def get_text_from_portfolio_company_of_vc(url):
    try:
        raw_text = scrap_portfolio_website(url)
        if raw_text == "":
            return "-"
        cleaned_text = clean_text(raw_text)
        return cleaned_text
    except Exception as e:
        print(e)


def get_info_about_vc_portfolio_startups(portfolio_url):
    try:
        startups_result_info = []

        # get portfolio startups links
        portfolio_startups_links = get_portfolio_links(portfolio_url)
        print(f"Portfolio links: {portfolio_startups_links} for startup {url}")

        # get text from startups website
        for portfolio_startup_link in portfolio_startups_links:
            text_from_startup_website = get_text_from_portfolio_company_of_vc(portfolio_startup_link)
            if text_from_startup_website == "-":
                continue
            else:
                print(f"Text from startup {portfolio_startup_link} website: {text_from_startup_website}")

                # get name of startup from website text
                name = repeat_gpt_answer_5_time(gpt_info_via_text, text_from_startup_website, schemas.VC_PORTFOLIO_STARTUP_NAME_RESPONSE_SCHEMA, constants.NAME_QUESTION)
                print(f"Name of startup {name}")

                # get solution from startup website text
                solution = repeat_gpt_answer_5_time(gpt_info_via_text, text_from_startup_website, schemas.VC_PORTFOLIO_STARTUP_SOLUTION_RESPONSE_SCHEMA, constants.SOLUTION_QUESTION)
                print(f"Name of startup {solution}")


        return startups_result_info
    except Exception as error:
        logging.error(f"Error during getting info about startup processing URL {url}: {error}")


if __name__ == "__main__":
    print("AI Powered Chat")

    combined_list = [
        ('https://9unicorns.in', 'https://9unicorns.in/portfolio.html'),
        ('https://constructcap.com/', 'https://constructcap.com/#investments'),
        ('https://correlationvc.com/', 'https://correlationvc.com/companies/'),
        ('https://cosmicapital.com/', 'https://www.karista.vc/portfolio'),
        ('https://cotacapital.com', 'https://www.cotacapital.com/portfolio/'),
        ('https://cptcap.com/', 'https://cptcap.com/investments/')
    ]

    for url, portfolio_url in combined_list:
        # industries, stages = get_info_about_vc(url)
        get_info_about_vc_portfolio_startups(portfolio_url)

        # TODO put all this data to our DB(sql)

        # TODO get data from sql(csv)

        # TODO "feed" new model with this data and get new, last answer

        # last answer should be like this
        # ```json
        # {
        # 	"Fund name": "Brooks Hill Partners",
        # 	"Fund website": "https://www.brookshillpartners.com/",
        # 	"Analyst name": "Neta Kafka",
        # 	"Analyst linkedin": "http://www.linkedin.com/in/nick-arrowsmith-2850131a4",
        # 	"Individual email message": "Dear Neta Kafka,
        #
        # I am writing to you to inquire about the possibility of investing in my startup. My startup is a medtech/biotech company that 3D prints bones to help treat bone cancer, helping both pharma and oncologists. We are currently at the pre-seed stage.
        #
        # I am aware that Brooks Hill Partners has invested in similar startups in the past, such as Cake (cake.com), ProCredEx (procredex.com), and Wasabi (wasabi.com). I believe that my startup is a great fit for your portfolio and I would love to discuss the possibility of investing in my startup.
        #
        # I look forward to hearing from you.
        #
        # Sincerely,
        # [Your Name]
        # "
        # }


        # ```

