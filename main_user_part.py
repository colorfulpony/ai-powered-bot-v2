import json
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

import openai
import streamlit as st

from check_if_fund_will_invest_in_user_startup import check_if_fund_will_invest_in_user_startup
from find_fund_info_by_vc_id import get_fund_info_by_vc_id
from find_matching_vcs_id import find_matching_vcs
from get_info_about_fund import get_info_about_fund
from refactor_output import refactor_output

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


# Set Streamlit title
st.title('🦜🔗 Project X')


# Main Function
def generate_response(startup_name, startup_stages, startup_industries, problems_solved):
    """
    Generate last response to user

    Parameters:
        startup_name (str): Name of user's startup.
        startup_stages (str): Stages in which user's startup works.
        startup_industries (str): Industries in which user's startup works.
        problems_solved (str): Problems that user's startup solves.
    """
    amount_of_funds = 0

    # Load JSON data
    with open("jsons/main.json") as f:
        data = json.load(f)

    # Split startup industries and stages into lists
    startup_industries = startup_industries.split(', ')
    startup_stages = startup_stages.split(', ')

    results = []
    # Create sentence about user's startup
    query = f"{startup_name} is a startup that works at {', '.join(str(item) for item in startup_stages)} stage in the {', '.join(str(item) for item in startup_industries)} industry. {startup_name} startup summary: {problems_solved}."

    # Find matching VCs based on industries and stages
    vcs_id = find_matching_vcs(user_industries=startup_industries, user_stages=startup_stages, json_data=data)
    print(vcs_id)

    # Get final answer iterating through each vc_id
    if vcs_id is not None:
        for vc_id in vcs_id:
            if amount_of_funds < 10:
                result = {}

                # Get fund info based on VC ID
                fund_info = get_fund_info_by_vc_id(vc_id['vc_id'])

                if fund_info is not None:
                    # Check if fund will invest in user's startup based on startups from vc's portfolio
                    fund_name = check_if_fund_will_invest_in_user_startup(query, fund_info)
                    print(fund_name)
                    if fund_name is not None:
                        if "no" in fund_name.lower():
                            continue
                        elif fund_name.startswith("Yes"):
                            # Get final answer -> Email to vc's analyst
                            raw_info = get_info_about_fund(query, fund_info)
                            print(raw_info)
                        else:
                            continue
                        if raw_info is None:
                            continue
                        else:
                            if not raw_info.startswith("I don't know"):
                                # Find the index of the last comma before }
                                index = raw_info.rfind(',')

                                # Remove the comma
                                raw_info = raw_info[:index] + raw_info[index + 1:]

                                # Refactor output
                                individual_email_message = refactor_output(raw_info)
                                print(individual_email_message)
                            else:
                                print(raw_info)

                            # Create final Results
                            result["Fund name"] = fund_info["vc_name"]
                            result["Fund website"] = fund_info["vc_website_url"]
                            result["Analyst name"] = fund_info["vc_investor_name"]
                            result["Analyst email"] = fund_info["vc_investor_email"]
                            result["Individual email message"] = individual_email_message["Individual email message"]
                            results.append(result)
                            amount_of_funds += 1
                    else:
                        continue
                else:
                    continue
            else:
                break

        # Display results
        st.title("Investment Fund Matches")
        if results:
            for entry in results:
                st.subheader(entry['Fund name'])
                st.markdown("**Fund website:** " + entry['Fund website'])
                st.markdown("**Analyst name:** " + entry['Analyst name'])
                st.markdown("**Analyst email:** " + entry['Analyst email'])
                st.markdown("**Individual email message:**")
                st.write(entry['Individual email message'])
                st.write("---")
        else:
            st.write("Sorry, we don't have matching funds for your startup in our dataset :(")
            st.write("---")
    else:
        st.write("Sorry, we don't have matching funds for your startup in our dataset :(")
        st.write("---")


with st.form('my_form'):
    # User inputs
    startup_name = st.text_input('Enter your startup name:')
    startup_industry = st.text_input('Enter your startup industry(s):')
    startup_stage = st.text_input('Enter your startup stage(s):')
    problems_solved = st.text_area('Enter solution of a problem that your startup solves:')

    submitted = st.form_submit_button('Submit')
    if submitted:
        st.markdown("---")
        st.write("Processing output...")

        # Get information for output
        generate_response(startup_name, startup_stage, startup_industry, problems_solved)
    else:
        st.write("---")


# Example usage
# startup_name = "Juko"
# startup_industry = "Finance, automation, money"
# startup_stage = "Seed, early-stage, and Series A"
# problems_solved = "It solves the user problem of automating key areas of business operations such as invoicing, payment collections, bulk payouts, GST filing, and customer data management."
#
# generate_response(startup_name, startup_stage, startup_industry, problems_solved)
