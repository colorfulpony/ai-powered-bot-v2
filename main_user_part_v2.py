import json
import os

import streamlit as st
import openai

from get_info_about_fund2 import get_info_about_fund
from refactor_output import refactor_output
from find_matching_vcs_id import find_matching_vcs_id
from find_fund_info_by_vc_id import get_fund_info_by_vc_id
from get_fund_name_that_will_invest_into_startup import get_fund_name_that_will_invest_into_startup


st.title('🦜🔗 Project X')


def generate_response(startup_name, startup_stage, startup_industry, problems_solved):
    with open("./json/test.json") as f:
        data = json.load(f)

    results = []
    query = f"{startup_name} is a startup that works at {startup_stage} stage in the {startup_industry} industry. {startup_name} startup summary: {problems_solved}."
    vcs_id = find_matching_vcs_id(user_industries=startup_industry, user_stages=startup_stage, json_data=data)

    if vcs_id is not None:
        for vc_id in vcs_id:
            result = {}
            fund_info = get_fund_info_by_vc_id(vc_id)
            if fund_info is not None:
                fund_name = get_fund_name_that_will_invest_into_startup(query, fund_info)
                print(fund_name)
                if fund_name is not None:
                    if "no" in fund_name.lower():
                        continue
                    elif fund_name.startswith("Yes, similar startups are"):
                        similar_startups = fund_name.split(": ")[1]
                        raw_info = get_info_about_fund(fund_name, query, fund_info, similar_startups)
                    else:
                        continue
                    if raw_info is None:
                        continue
                    else:
                        individual_email_message = refactor_output(raw_info)
                        result["Fund name"] = fund_info["vc_name"]
                        result["Fund website"] = fund_info["vc_website_url"]
                        result["Analyst name"] = fund_info["vc_investor_name"]
                        result["Analyst email"] = fund_info["vc_investor_email"]
                        result["Individual email message"] = individual_email_message["Individual email message"]
                        results.append(result)
                else:
                    continue
            else:
                continue

        st.title("Investment Fund Matches")
        print(results)
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
    startup_name = st.text_input('Enter your startup name:')
    startup_industry = st.text_input('Enter your startup industry(s):')
    startup_stage = st.text_input('Enter your startup stage(s):')
    problems_solved = st.text_area('Enter solution of a problem that your startup solves:')

    submitted = st.form_submit_button('Submit')
    if submitted:
        st.markdown("---")
        st.write("Processing output...")
        generate_response(startup_name, startup_stage, startup_industry, problems_solved)
    else:
        st.write("---")
