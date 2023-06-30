import json

# Read JSON from file
with open('jsons/main.json', 'r') as json_file:
    data = json.load(json_file)

# Function to get fund information by vc_id
def get_fund_info_by_vc_id(vc_id):
    """
    Get fund information by venture capital ID.

    Parameters:
        vc_id (int): The venture capital ID.

    Returns:
        dict: The fund information if found, or None if not found.
    """
    # Iterate over venture capitals
    for vc_key, vc_data in data.items():
        if vc_data['vc_id'] == vc_id:  # Check if vc_id matches
            return vc_data  # Return the fund information

    return None  # Return None if the vc_id is not found
