import json

# Read JSON from file
with open('json/test.json', 'r') as json_file:
    data = json.load(json_file)

# Function to get fund information by vc_id
def get_fund_info_by_vc_id(vc_id):
    # Iterate over venture capitals
    for vc in data['venture_capitals']:
        for vc_key, vc_data in vc.items():
            if vc_data['vc_id'] == vc_id:  # Check if vc_id matches
                return vc_data  # Return the fund information

    return None  # Return None if the vc_id is not found
