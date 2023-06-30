import traceback
import gspread


def get_data_from_google_sheets(data_range):
    """
    Get data from a Google Sheets worksheet.

    Parameters:
        data_range (str): The range of cells to retrieve data from (e.g., 'A1:C10').

    Returns:
        list: A list of tuples representing the rows of data.
    """
    try:
        # Connection To Worksheet
        gc = gspread.service_account('../secrets.json')
        spreadsheet = gc.open('Working')
        worksheet = spreadsheet.worksheet('Copy of Companies Main')

        # Get the values from the specified range
        range_values = worksheet.get(data_range)

        # Create a list to store the rows
        rows = []

        # Iterate over the range values and append each row to the list
        for row in range_values:
            row_data = tuple(row)  # Convert the row list to a tuple
            rows.append(row_data)

        return rows
    except Exception as e:
        print(e)
        traceback.print_exc()
        return None
