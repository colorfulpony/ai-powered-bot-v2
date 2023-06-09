from flask import Flask, render_template, request, jsonify
from get_info_about_fund import get_info_about_fund
from matched_fund_names import get_matched_fund_names
from refactor_output import refactor_output

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    startup_name = request.form['startup_name']
    startup_stage = request.form['startup_stage']
    startup_industry = request.form['startup_industry']
    problems_solved = request.form['problems_solved']

    query = f"{startup_name} is a startup that works at {startup_stage} stage(s) in the {startup_industry} industry(s) that solves the following problems: {problems_solved}."
    fund_names = get_matched_fund_names(query)

    if fund_names.startswith("Sorry, try again"):
        return jsonify({'error': fund_names}), 400
    else:
        fund_names = fund_names.split(", ")
        results = []
        for fund_name in fund_names:
            raw_result = get_info_about_fund(fund_name, query)
            result = refactor_output(raw_result)
            results.append(result)
        return jsonify(results), 200


if __name__ == '__main__':
    app.run()
