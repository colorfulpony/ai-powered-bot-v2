import traceback
import gspread


async def insert_data_into_google_sheets(data):
    """
    Insert data into a Google Sheets worksheet.

    Parameters:
        data (list): A list of lists representing the data to be inserted.

    """
    try:
        # Connection To Worksheet
        gc = gspread.service_account('../secrets.json')
        spreadsheet = gc.open('Structured data')
        worksheet = spreadsheet.worksheet('Copy of Structured data')

        last_row_index = len(worksheet.get_all_values()) + 1

        # Construct the data range
        data_range = f'A{last_row_index}:J{last_row_index + len(data) - 1}'

        # Insert data into the next empty row
        worksheet.update(data_range, data)
    except Exception as e:
        print(e)
        traceback.print_exc()
