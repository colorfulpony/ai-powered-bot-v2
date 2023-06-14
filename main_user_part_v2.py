import os

import streamlit as st
from flask import jsonify
import openai

from get_info_about_fund import get_info_about_fund
from matched_fund_names import get_matched_fund_names
from refactor_output import refactor_output

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Access the API key and use it in API requests
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

st.title('🦜🔗 Project X')


def generate_response(startup_name, startup_stage, startup_industry, problems_solved):
    results = []
    query = f"{startup_name} is a startup that works at {startup_stage} stage(s) in the {startup_industry} industry(s) that solves the following problems: {problems_solved}."
    fund_names = get_matched_fund_names(query)

    if fund_names.startswith("Sorry, try again"):
        return jsonify({'error': fund_names}), 400
    else:
        fund_names = fund_names.split(", ")
        for fund_name in fund_names:
            raw_result = get_info_about_fund(fund_name, query)
            result = refactor_output(raw_result)
            results.append(result)
            # return jsonify(result), 200
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
