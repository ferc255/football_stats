"""
The module fetches updates from the source file and recreates database.
"""
from foostats.utils.api_requests import get_api_service


def main():
    """
    The main function of the utility.
    """
    service = get_api_service()

    spreadsheet_id = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    range_name = 'Class Data!A2:E'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                 range=range_name).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
    for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        print('%s, %s' % (row[0], row[4]))


if __name__ == '__main__':
    main()
