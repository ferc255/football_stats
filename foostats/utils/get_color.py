"""
The module fetches updates from the source file and recreates database.
"""
from foostats.tools.api_requests import get_api_service


def main():
    """
    The main function of the utility.
    """
    service = get_api_service()

    spreadsheet_id = '1QH-AFYHk3lXJf-dG3FzhDwtO6iJZus7ZXWoY8aBs7ZI'
    range_name = '05/18!A2:C4'

    result = service.spreadsheets().get(spreadsheetId=spreadsheet_id,
                                        ranges=range_name,
                                        includeGridData=True).execute()

    print(result['sheets'][0]['data'][0]['rowData'][0]['values'][0])


if __name__ == '__main__':
    main()
