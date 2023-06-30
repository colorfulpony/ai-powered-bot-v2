import csv
import json

csv_file_path = "../csvs/main.csv"
json_file_path = '../jsons/test.jsons'

data = {}

# Read the CSV file and group startups under each VC
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for line_num, row in enumerate(reader, start=1):
        try:
            fund_name = row['vc_name']
            vc_data = data.get(fund_name)

            if vc_data is None:
                vc_data = {
                    'vc_name': fund_name,
                    'vc_website_url': row['vc_website_url'],
                    'vc_linkedin_url': row['vc_linkedin_url'],
                    'vc_investor_name': row['vc_investor_name'],
                    'vc_investor_email': row['vc_investor_email'],
                    'vc_stages': row['vc_stages'],
                    'vc_industries': row['vc_industries'],
                    'vc_portfolio': []
                }
                data[fund_name] = vc_data

            startup = {
                'vc_portfolio_startup_name': row['vc_portfolio_startup_name'],
                'vc_portfolio_startup_website_url': row['vc_portfolio_startup_website_url'],
                'vc_portfolio_startup_solution': row['vc_portfolio_startup_solution'],
                'vc_portfolio_startup_id': len(vc_data['vc_portfolio']) + 1
            }

            vc_data['vc_portfolio'].append(startup)
        except UnicodeDecodeError:
            print(f"UnicodeDecodeError occurred in line {line_num}")

# Add index for each VC
for vc_id, (fund_name, vc_data) in enumerate(data.items(), start=1):
    vc_data['vc_id'] = vc_id

# Convert the data to JSON format
json_data = json.dumps(data, indent=4)

# Save the JSON data to a file
with open(json_file_path, 'w') as jsonfile:
    jsonfile.write(json_data)
