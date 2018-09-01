"""
The module fetches updates from the source file and recreates database.
"""
import re
import sys
import json
from foostats.utils.api_requests import get_api_service
from foostats.settings import SOURCE_SPREADSHEET_ID
from foostats.utils.api_requests import with_async_state


def parse_score(score):
    score = score.strip()
    score = [int(num) for num in re.split('[ -]+', score)]
    score = sorted(score, reverse=True)
    return score


def reverse_date(date):
    date = date.strip()
    date = date.split('.')
    date = '.'.join(reversed(date))
    return date


def fetch(month):
    matches = {}
    for i, date in enumerate(month[0]['values']):
        if not i or not date.get('formattedValue'):
            continue

        match = {
            'score': parse_score(
                month[1]['values'][i]['formattedValue']),
            'red': [],
            'green': [],
            'blue': [],
        }

        for j, player in enumerate(month):
            if j < 4 or not player['values'][i].get('formattedValue'):
                continue

            if match['score'][0] != match['score'][1]:
                player_score = int(player['values'][i]['formattedValue'])
                index = match['score'].index(player_score)

                if len(match['score']) == 2:
                    player_color = 'red' if index == 0 else 'blue'
                else:
                    if index == 0:
                        player_color = 'red'
                    elif index == 1:
                        player_color = 'green'
                    else:
                        player_color = 'blue'
            else:
                player_color = (
                    player['values'][i]['effectiveFormat']['backgroundColor'])
                assert (bool(player_color.get('red')) ^
                        bool(player_color.get('blue')))
                player_color = 'red' if player_color.get('red') else 'blue'

            match[player_color].append(
                player['values'][0]['formattedValue'])

        date = reverse_date(date['formattedValue'])
        matches[date] = match

    return matches


@with_async_state
def get_year_stats(service):
    result = service.spreadsheets().get(spreadsheetId=SOURCE_SPREADSHEET_ID,
                                        includeGridData=True).execute()
    result = [sheet['data'][0]['rowData']
              for sheet in result['sheets']
              if sheet['properties']['title'].strip().endswith('/18')]
    return result


def main():
    """
    The main function of the utility.
    """
    service = get_api_service()

    year_stats = get_year_stats(service)

    matches = {}
    for month in year_stats:
        matches.update(fetch(month))

    json.dump(matches, open(sys.argv[1], 'w'), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
