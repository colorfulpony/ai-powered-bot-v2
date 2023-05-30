import gspread


def insert_data_into_google_sheets(vc_name, vc_website_url, vc_linkedin_url, vc_investor_name, vc_investor_email, vc_stages, vc_industries, portfolio_websites_data):
    # Connection To Worksheet
    gc = gspread.service_account('secrets.json')
    spreadsheet = gc.open('Structured data')
    worksheet = spreadsheet.worksheet('Structured data')

    if not vc_name:
        vc_name = "-"

    if not vc_website_url:
        vc_website_url = "-"

    if not vc_linkedin_url:
        vc_linkedin_url = "-"

    if not vc_investor_name:
        vc_investor_name = "-"

    if not vc_investor_email:
        vc_investor_email = "-"

    if not vc_stages:
        vc_stages = "-"

    if not vc_industries:
        vc_industries = "-"

    data = [vc_name, vc_website_url, vc_linkedin_url, vc_investor_name, vc_investor_email, vc_stages, vc_industries]

    # Get the index of the last unused row
    if portfolio_websites_data:
        for portfolio_website_data in portfolio_websites_data:
            new_data = list(data)
            last_row_index = len(worksheet.get_all_values()) + 1

            new_data.append(portfolio_website_data[0])
            new_data.append(portfolio_website_data[1])
            new_data.append(portfolio_website_data[2])

            worksheet.insert_row(new_data, last_row_index)
    else:
        new_data = list(data)
        last_row_index = len(worksheet.get_all_values()) + 1

        new_data.append(data + list(("-", "-", "-")))

        worksheet.insert_row(new_data, last_row_index)
