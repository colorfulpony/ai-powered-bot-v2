import json
import re


def refactor_output(string_data):
    # Remove the word 'json' from the string
    string_data = string_data.replace('```', '')
    string_data = string_data.replace('json', '')

    # Remove invalid control characters
    string_data = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', string_data)

    # Parse the modified string as JSON
    json_data = json.loads(string_data)

    return json_data
