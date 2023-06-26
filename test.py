import json
import os

import openai
import os

import streamlit as st
import openai

from get_info_about_fund import get_info_about_fund

from get_fund_name_that_will_invest_into_startup import get_fund_name_that_will_invest_into_startup
from get_info_about_fund2 import get_info_about_fund
from refactor_output import refactor_output
from find_matching_vcs_id import find_matching_vcs_id
from find_fund_info_by_vc_id import get_fund_info_by_vc_id

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Access the API key and use it in API requests
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

def generate_response(startup_name, startup_stage, startup_industry, problems_solved):
    with open("./json/test.json") as f:
        data = json.load(f)

    results = []
    query = f"{startup_name} is a startup that works at {startup_stage} stage in the {startup_industry} industry. {startup_name} startup summary: {problems_solved}."

    vcs_id = find_matching_vcs_id(user_industries=startup_industry, user_stages=startup_stage, json_data=data)

    for vc_id in vcs_id:
        fund_info = get_fund_info_by_vc_id(vc_id)
        fund_name = get_fund_name_that_will_invest_into_startup(query, fund_info)
        # print(fund_name)
        if "no" in fund_name.lower():
            continue
        elif fund_name.startswith("Yes, similar startups are"):
            similar_startups = fund_name.split(": ")[1]
            raw_info = get_info_about_fund(fund_name, query, fund_info, similar_startups)
        else:
            raw_info = get_info_about_fund(fund_name, query, fund_info)
        result = refactor_output(raw_info)
        print(result)
        # results.append(result)


if __name__ == '__main__':
    startup_name = "Juko"
    startup_industry = "Finance, automation, money"
    startup_stage = "Seed, early-stage, and Series A"
    problems_solved = "It solves the user problem of automating key areas of business operations such as invoicing, payment collections, bulk payouts, GST filing, and customer data management."

    test = generate_response(startup_name, startup_stage, startup_industry, problems_solved)