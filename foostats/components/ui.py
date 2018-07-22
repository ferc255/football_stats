import sys
import json
import random

from foostats.utils.api_requests import get_api_service
from foostats.utils.api_requests import with_async_state
from foostats.settings import SPREADSHEET_ID, MAXIMUM_CELL_BRIGHTNESS


@with_async_state
def batch_update(service, body):
    """
    Service function which does batchUpdate
    """
    service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID,
                                       body=body).execute()


def update_sheet_widths(service, sheet_id, widths):
    def create_request(column, width):
        return {
            'range': {
                'sheetId': sheet_id,
                'dimension': 'COLUMNS',
                'startIndex': column,
                'endIndex': column + 1,
            },
            'properties': {
                'pixelSize': width,
            },
            'fields': 'pixelSize',
        }

    body = [
        {'updateDimensionProperties': create_request(column, width)}
        for column, width in enumerate(widths)
    ]

    batch_update(service, {'requests': body})


def clear_sheet(service, sheet_id):
    sheet_range = {
        'sheetId': sheet_id,
        'startRowIndex': 0,
        'endRowIndex': 1000,
        'startColumnIndex': 0,
        'endColumnIndex': 30
    }
    body = {
        'requests': [
            {
                'repeatCell': {
                    'range': sheet_range,
                    'fields': '*',
                },
            },
            {
                'unmergeCells': {
                    'range': sheet_range,
                },
            },
        ]
    }

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


def gen_color():
    return {
        'red': 1 - random.uniform(0, MAXIMUM_CELL_BRIGHTNESS),
        'green': 1 - random.uniform(0, MAXIMUM_CELL_BRIGHTNESS),
        'blue': 1 - random.uniform(0, MAXIMUM_CELL_BRIGHTNESS),
    }


class Table:
    title_font_size = 14
    description_font_size = 10
    colnames_font_size = 12
    data_font_size = 12
    name_align = 'LEFT'
    values_align = 'CENTER'

    def __init__(self, header, data, columns, color):
        self.title = header['title']
        self.description = header['description']
        self.colnames = header['colnames']
        self.data = data
        self.columns = columns
        self.color = color

    @staticmethod
    def merge_cells(sheet_id, start_row, start_column,
                    end_row, end_column):
        request = {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_column,
                'endColumnIndex': end_column,
            },
            'mergeType': 'MERGE_ROWS',
        }

        return {'mergeCells': request}

    def construct_value(self, text, alignment, font_size, bold):
        return {
            'userEnteredValue': {
                'stringValue': str(text),
            },
            'userEnteredFormat': {
                'backgroundColor': {
                    'red': self.color['red'],
                    'green': self.color['green'],
                    'blue': self.color['blue'],
                },
                'textFormat': {
                    'fontSize': font_size,
                    'bold': bold,
                },
                'horizontalAlignment': alignment,
                'wrapStrategy': 'WRAP',
            },
        }

    def update_cells(self, sheet_id, data, position, style):
        request = {
            'fields': '*',  # Shouldn't be *. Though...
            'start': {
                'sheetId': sheet_id,
                'row_index': position['row_index'],
                'column_index': position['column_index'],
            },
            'rows': [],
        }

        alignment = style.pop('alignment')
        for row in data:
            values = []
            for i, col in enumerate(row):
                if isinstance(alignment, list):
                    align = alignment[i]
                else:
                    align = alignment

                values.append(
                    self.construct_value(col, align, **style)
                )
            request['rows'].append({'values': values})

        return {'updateCells': request}

    @staticmethod
    def set_borders(sheet_id, start_row, start_column,
                    end_row, end_column):
        style = {
            'style': 'SOLID',
            'width': 1,
        }
        request = {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'startColumnIndex': start_column,
                'endRowIndex': end_row,
                'endColumnIndex': end_column,
            },
            'top': style,
            'bottom': style,
            'left': style,
            'right': style,
            'innerHorizontal': style,
            'innerVertical': style,
        }

        return {'updateBorders': request}

    def draw(self, service, sheet_id, corner_cell):
        row_index = int(corner_cell[1:]) - 1
        column_index = ord(corner_cell[0]) - ord('A')
        requests = []

        # Title
        requests.append(
            self.update_cells(
                sheet_id, [[self.title]],
                {
                    'row_index': row_index,
                    'column_index': column_index,
                },
                {
                    'alignment': 'CENTER',
                    'font_size': self.title_font_size,
                    'bold': True,
                },
            )
        )

        # Description
        requests.append(
            self.update_cells(
                sheet_id, [[self.description]],
                {
                    'row_index': row_index + 1,
                    'column_index': column_index,
                },
                {
                    'alignment': 'LEFT',
                    'font_size': self.description_font_size,
                    'bold': False,
                },
            )
        )

        # Colnames
        requests.append(
            self.update_cells(
                sheet_id, [self.colnames],
                {
                    'row_index': row_index + 2,
                    'column_index': column_index,
                },
                {
                    'alignment': 'CENTER',
                    'font_size': self.colnames_font_size,
                    'bold': True,
                },
            )
        )

        # Data
        requests.append(
            self.update_cells(
                sheet_id, self.data,
                {
                    'row_index': row_index + 3,
                    'column_index': column_index,
                },
                {
                    'alignment': ['LEFT', 'CENTER'],
                    'font_size': self.data_font_size,
                    'bold': False,
                },
            )
        )

        # Borders
        requests.append(
            self.set_borders(
                sheet_id, row_index, column_index,
                row_index + len(self.data) + 3, column_index + self.columns,
            )
        )

        # Merge
        requests.append(
            self.merge_cells(
                sheet_id, row_index, column_index, row_index + 2,
                column_index + self.columns,
            )
        )

        batch_update(service, {'requests': requests})


def main():
    stats = json.load(open(sys.argv[1]))

    service = get_api_service()

    main_id = get_main_id(service)

    clear_sheet(service, main_id)

    first_table_header = {
        'title': 'Всего очков',
        'description': ('Большой и длинный дескрипшн дабы '
                        'проверить что все у нас хорошо '
                        'и что у нас работает перенос по '
                        'словам.'),
        'colnames': ['Игрок', 'Очков'],
    }
    first_table = Table(first_table_header,
                        data=stats['MAIN']['total_points']['data'],
                        columns=stats['MAIN']['total_points']['columns'],
                        color=gen_color())
    first_table.draw(service, main_id, 'A3')

    update_sheet_widths(service, main_id, [200] * 2)


if __name__ == '__main__':
    main()
