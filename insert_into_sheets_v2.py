import traceback
import gspread


async def insert_data_into_google_sheets(data):
    try:
        # Connection To Worksheet
        gc = gspread.service_account('secrets.json')
        spreadsheet = gc.open('Structured data')
        worksheet = spreadsheet.worksheet('Structured data')

        last_row_index = len(worksheet.get_all_values()) + 1

        # Construct the data range
        data_range = f'A{last_row_index}:K{last_row_index + len(data) - 1}'

        # Insert data into the next empty row
        worksheet.update(data_range, data)
    except Exception as e:
        print(e)
        traceback.print_exc()


def get_wait_time(api_error):
    default_wait_time = 60  # Fallback wait time in seconds if Retry-After header is not available
    try:
        return int(api_error.response.headers["Retry-After"])
    except (KeyError, ValueError):
        return default_wait_time

