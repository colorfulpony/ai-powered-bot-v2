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

st.title('🦜🔗 Project X')


def generate_response(startup_name, startup_stage, startup_industry, problems_solved):
    with open("./json/test.json") as f:
        data = json.load(f)

    results = []
    query = f"{startup_name} is a startup that works at {startup_stage} stage in the {startup_industry} industry. {startup_name} startup summary: {problems_solved}."

    vcs_id = find_matching_vcs_id(user_industries=startup_industry, user_stages=startup_stage, json_data=data)

    for vc_id in vcs_id:
        fund_info = get_fund_info_by_vc_id(vc_id)
        fund_name = get_fund_name_that_will_invest_into_startup(query, fund_info)
        raw_info = get_info_about_fund(fund_name, query, fund_info)
        result = refactor_output(raw_info)
        results.append(result)

    st.title("Investment Fund Matches")

    for entry in results:
        st.subheader(entry['Fund name'])
        st.markdown("**Fund website:** " + entry['Fund website'])
        st.markdown("**Analyst name:** " + entry['Analyst name'])
        st.markdown("**Analyst LinkedIn:** " + entry['Analyst linkedin'])
        st.markdown("**Individual email message:**")
        st.write(entry['Individual email message'])
        st.write("---")


with st.form('my_form'):
    startup_name = st.text_input('Enter your startup name:')
    startup_stage = st.text_input('Enter your startup industry(s):')
    startup_industry = st.text_input('Enter your startup stage(s):')
    problems_solved = st.text_area('Enter solution of a problem that your startup solves:')

    submitted = st.form_submit_button('Submit')
    if submitted:
        st.markdown("---")
        st.write("Processing output...")
        generate_response(startup_name, startup_stage, startup_industry, problems_solved)
    else:
        st.write("---")
