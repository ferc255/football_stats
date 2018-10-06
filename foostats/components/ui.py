import random

from foostats.utils.api_requests import get_api_service
from foostats.utils.api_requests import with_async_state
from foostats.settings import SPREADSHEET_ID, MAXIMUM_CELL_BRIGHTNESS
from foostats.utils.helpers import get_logger


LOGGER = get_logger(__name__)


@with_async_state
def batch_update(service, body):
    """
    Service function which does batchUpdate
    """
    return service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID,
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


def clear_sheet(sheet_id):
    return [
        {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                },
                'fields': '*',
            },
        },
        {
            'unmergeCells': {
                'range': {
                    'sheetId': sheet_id,
                }
            },
        },
    ]


@with_async_state
def get_all_sheets(service):
    return service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID).execute()['sheets']


def init(service):
    sheets = get_all_sheets(service)

    temp_sheet_id = None
    body = []
    for sheet in sheets:
        if sheet['properties']['title'] == '_temp':
            temp_sheet_id = sheet['properties']['sheetId']
        else:
            body.append({
                'deleteSheet': {
                    'sheetId': sheet['properties']['sheetId'],
                }
            })

    if not temp_sheet_id:
        temp_sheet_id = batch_update(
            service,
            {
                'requests': {
                    'addSheet': {
                        'properties': {
                            'title': '_temp',
                            'gridProperties': {
                                'columnCount': 1,
                                'rowCount': 1,
                            }
                        }
                    }
                }
            }
        )['replies'][0]['addSheet']['properties']['sheetId']

    batch_update(service, {'requests': body})

    main_id = batch_update(
        service,
        {
            'requests': {
                'addSheet': {
                    'properties': {
                        'title': 'MAIN',
                        'gridProperties': {
                            # Later I should add rowCount.
                            # I need to find out how much lines it requires,
                            # and remove trailing empty lines out of concern
                            # for performance deterioration.
                            'columnCount': 6,
                        }
                    }
                }
            }
        }
    )['replies'][0]['addSheet']['properties']['sheetId']

    batch_update(
        service,
        {
            'requests': {
                'deleteSheet': {
                    'sheetId': temp_sheet_id,
                }
            }
        }
    )

    return main_id


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
    data_alignment = 'CENTER'

    def __init__(self, header, data, columns, color):
        self.title = header['title']
        self.description = header['description']
        self.colnames = header['colnames']
        self.data = data
        self.columns = columns
        self.color = color

    @classmethod
    def build_table(cls, table_name, header, data, alignment):
        result = cls(
            header,
            data=data[table_name]['data'],
            columns=data[table_name]['columns'],
            color=gen_color())
        result.data_alignment = alignment
        return result

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
                'verticalAlignment': 'MIDDLE',
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
                    'alignment': self.data_alignment,
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


def create_sheets(service, stats):
    result = {'MAIN': init(service)}
    body = []
    for player in sorted(stats):
        if player != 'MAIN':
            body = {
                'requests': {
                    'addSheet': {
                        'properties': {
                            'title': player,
                            'gridProperties': {
                                'columnCount': 6,  # Attention!!!
                            }
                        }
                    }
                }
            }

            LOGGER.info('Creating empty sheet for %s', player)
            # We must do every creation as a separate batch_update
            # because we want to get all the sheets in an alphabetical order.
            result[player] = (
                batch_update(service, body)
                ['replies'][0]['addSheet']['properties']['sheetId']
            )

    return result


def draw(stats):
    """
    Valid request:
        python3 components/ui.py database/processed.json
    """
    LOGGER.info('Getting api service for drawing')
    service = get_api_service()

    LOGGER.info('Creating sheets for each player')
    sheet_id = create_sheets(service, stats)

    LOGGER.info('Filling the MAIN sheet')
    total_points = Table.build_table(
        'total_points',
        {
            'title': 'Всего очков',
            'description': ('Большой и длинный дескрипшн дабы '
                            'проверить что все у нас хорошо '
                            'и что у нас работает перенос по '
                            'словам.'),
            'colnames': ['Игрок', 'Очков'],
        },
        stats['MAIN'],
        ['LEFT', 'CENTER']
    )
    total_points.draw(service, sheet_id['MAIN'], 'A3')

    player_tables = {}
    for player in stats:
        if player != 'MAIN':
            player_tables[player] = {
                'coef_history': Table.build_table(
                    'coef_history',
                    {
                        'title': 'История коэффициента очков',
                        'description': (
                            'Большой и длинный дескрипшн дабы '
                            'проверить что все у нас хорошо '
                            'и что у нас работает перенос по '
                            'словам.'),
                        'colnames': ['N', 'Дата', 'Место в рейтинге',
                                     'Процент очков',
                                     'Кого обогнал в рейтинге',
                                     'Кому уступил в рейтинге'],
                    },
                    stats[player],
                    ['CENTER'] * 6
                )
            }

    for player in player_tables:
        LOGGER.info('Filling statistics for %s', player)
        player_tables[player]['coef_history'].draw(
            service, sheet_id[player], 'A3')

    LOGGER.info('Successfully drawn all the stats!')
    update_sheet_widths(service, sheet_id['MAIN'], [200] * 2)
