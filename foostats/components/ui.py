"""
The module fetches updates from the source file and recreates database.
"""
import sys
import json
from foostats.utils.api_requests import get_api_service
from foostats.utils.api_requests import with_async_state
from foostats.settings import SPREADSHEET_ID


@with_async_state
def batch_update(service, body):
    """
    Service function which does batchUpdate
    """
    service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID,
                                       body=body).execute()


def update_cells(service, sheet_id, corner_cell, table):
    """
    Fill the sheet with the data from the table, starting from
    corner_cell position.
    """
    column_index = ord(corner_cell[0]) - ord('A')
    row_index = int(corner_cell[1:]) - 1

    body = {
        'requests': [{
            'updateCells': {
                'fields': '*',
                'start': {
                    'sheetId': sheet_id,
                    'column_index': column_index,
                    'row_index': row_index,
                },
                'rows': [],
            }
        }]
    }

    for row in table:
        prepared_row = {'values': []}
        for col in row:
            prepared_row['values'].append({
                'userEnteredValue': {
                    'stringValue': str(col),
                }
            })
        body['requests'][0]['updateCells']['rows'].append(prepared_row)

    batch_update(service, body)


@with_async_state
def get_main_id(service):
    """
    Get sheetId of the MAIN page
    """
    response = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID).execute()

    for sheet in response['sheets']:
        if sheet['properties']['title'] == 'MAIN':
            return sheet['properties']['sheetId']

    return None


def main():
    """
    The main function of the module
    """
    stats = json.load(open(sys.argv[1]))

    service = get_api_service()
    main_id = get_main_id(service)

    first_table = [['Всего очков'], ['Description']]
    first_table.extend(stats['MAIN']['total_points'])
    update_cells(service, main_id, 'B3', first_table)


if __name__ == '__main__':
    main()
