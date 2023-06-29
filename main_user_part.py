import json
import os

import streamlit as st
import openai

from get_info_about_fund import get_info_about_fund
from refactor_output import refactor_output
from find_matching_vcs_id import find_matching_vcs
from find_fund_info_by_vc_id import get_fund_info_by_vc_id
from check_if_fund_will_invest_in_user_startup import check_if_fund_will_invest_in_user_startup


os.environ["OPENAI_API_KEY"] = "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"

# Access the API key and use it in API requests
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

# t.title('🦜🔗 Project X')


def generate_response(startup_name, startup_stages, startup_industries, problems_solved):
    amount_of_funds = 0
    with open("./json/main.json") as f:
        data = json.load(f)

    startup_industries = startup_industries.split(', ')
    startup_stages = startup_stages.split(', ')

    results = []
    query = f"{startup_name} is a startup that works at {', '.join(str(item) for item in startup_stages)} stage in the {', '.join(str(item) for item in startup_industries)} industry. {startup_name} startup summary: {problems_solved}."
    vcs_id = find_matching_vcs(user_industries=startup_industries, user_stages=startup_stages, json_data=data)
    print(vcs_id)

    if vcs_id is not None:
        for vc_id in vcs_id:
            if amount_of_funds < 5:
                result = {}
                fund_info = get_fund_info_by_vc_id(vc_id['vc_id'])
                if fund_info is not None:
                    fund_name = check_if_fund_will_invest_in_user_startup(query, fund_info)
                    print(fund_name)
                    if fund_name is not None:
                        if "no" in fund_name.lower():
                            continue
                        elif fund_name.startswith("Yes"):
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

                                individual_email_message = refactor_output(raw_info)
                            else:
                                print(raw_info)
                            print(individual_email_message)
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

#         st.title("Investment Fund Matches")
#         if results:
#             for entry in results:
#                 st.subheader(entry['Fund name'])
#                 st.markdown("**Fund website:** " + entry['Fund website'])
#                 st.markdown("**Analyst name:** " + entry['Analyst name'])
#                 st.markdown("**Analyst email:** " + entry['Analyst email'])
#                 st.markdown("**Individual email message:**")
#                 st.write(entry['Individual email message'])
#                 st.write("---")
#         else:
#             st.write("Sorry, we don't have matching funds for your startup in our dataset :(")
#             st.write("---")
#     else:
#         st.write("Sorry, we don't have matching funds for your startup in our dataset :(")
#         st.write("---")
#
#
# with st.form('my_form'):
#     startup_name = st.text_input('Enter your startup name:')
#     startup_industry = st.text_input('Enter your startup industry(s):')
#     startup_stage = st.text_input('Enter your startup stage(s):')
#     problems_solved = st.text_area('Enter solution of a problem that your startup solves:')
#
#     submitted = st.form_submit_button('Submit')
#     if submitted:
#         st.markdown("---")
#         st.write("Processing output...")
#         generate_response(startup_name, startup_stage, startup_industry, problems_solved)
#     else:
#         st.write("---")
#
if __name__ == '__main__':
    startup_name = "SIRPLUS"
    startup_industry = "B2C, Ecommerce, Climate Tech"
    startup_stage = "Seed"
    problems_solved = "It helps consumer to buy let over food from store at an attractive price to help reduce foodwaste and save the planet"
    generate_response(startup_name, startup_stage, startup_industry, problems_solved)