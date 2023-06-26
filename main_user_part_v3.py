from flask import jsonify
from get_info_about_fund import get_info_about_fund
from matched_fund_names import get_matched_fund_names
from refactor_output import refactor_output


def main(startup_name, startup_stage, startup_industry, problems_solved):
    query = f"{startup_name} is a startup that works at {startup_stage} stage(s) in the {startup_industry} industry(s) that solves the following problems: {problems_solved}."
    fund_names = get_matched_fund_names(query)

    if fund_names.startswith("Sorry, try again"):
        return jsonify({'error': fund_names}), 400
    else:
        fund_names = fund_names.split(", ")
        for fund_name in fund_names:
            raw_result = get_info_about_fund(fund_name, query)
            result = refactor_output(raw_result)
            print(result)
            # return jsonify(result), 200
