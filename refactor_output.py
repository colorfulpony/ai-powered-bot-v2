import json
import re


def refactor_output(string_data):
    """
    Refactor individual email message

    If in string_data we have something lie:
    ```json
        {
            "Individual email message": "Dear Kendahl Mitra,\n\nI hope this email finds you well. I am reaching out to you because I believe that Dayblink Ventures would be interested in investing in my startup, SIRPLUS. SIRPLUS is a Seed stage startup in the B2C, Ecommerce, Climet Tech industry that helps consumers buy food that will go waist at an affordable price, thus reducing the climate impact of food waste. I noticed that Dayblink Ventures has invested in Full Circle (fullcircle.com), a startup that also aims to solve the problem of people having access to fresh and organic produce. I believe that our missions align and that SIRPLUS would be a great addition to your portfolio. Thank you for your time and consideration.\n\nBest regards,\n[Your Name]"
        }
    ```

    Then after refactoring we should get json format but not string

    Parameters:
        string_data (str): Individual email msg.
    """
    # Remove the word 'jsons' from the string
    string_data = string_data.replace('```', '')
    string_data = string_data.replace('json', '')
    string_data = string_data.replace('jsons', '')

    # Remove invalid control characters
    string_data = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', string_data)

    # Parse the modified string as JSON
    json_data = json.loads(string_data)

    return json_data


