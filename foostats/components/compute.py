"""
Processes the set of games and returns statistics in json format, which
should be displayed in Google Spreadsheets in the future.
"""
import collections
import functools

from foostats.settings import MIN_MATCH_COUNT
from foostats.utils.helpers import get_logger


LOGGER = get_logger(__name__)


def get_players_set(matches):
    """
    Get list of all the players
    """
    players_set = set()
    for match in matches.values():
        for color in ['red', 'green', 'blue']:
            for player in match[color]:
                players_set.add(player)
    return players_set


def get_match_results(match):
    points = collections.defaultdict(int)
    if match['score'][0] == match['score'][1]:
        points_to_add = {
            'red': 1,
            'green': 1,
            'blue': 1,
        }
    else:
        points_to_add = {
            'red': 3,
            'green': 1,
            'blue': 0,
        }

    for color in ['red', 'green', 'blue']:
        for player in match[color]:
            points[player] += points_to_add[color]

    return {'points': points}


def get_total_points(matches):
    """
    Calculates everything so far
    """
    total_points = collections.defaultdict(int)
    for match in matches.values():
        for player, score in get_match_results(match)['points'].items():
            total_points[player] += score

    result = {
        'columns': 2,
        'data': []
    }
    for player, score in sorted(total_points.items(),
                                key=lambda x: (-x[1], x[0])):
        result['data'].append([player, score])
    return result


def get_coef_history(matches, player_name, min_matches_count):
    def comparator(first, second):
        if (bool(first['match_count'] >= min_matches_count) !=
                bool(second['match_count'] >= min_matches_count)):
            return -1 if first['match_count'] >= min_matches_count else 1
        if first['coef'] != second['coef']:
            return second['coef'] - first['coef']
        return -1 if first['name'] < second['name'] else 1

    players_set = get_players_set(matches)
    player_stats = {
        player: {
            'points': 0,
            'matches': 0,
        } for player in players_set
    }
    delta_set = {'prev': {}}
    result = []
    for date, match in sorted(matches.items(), key=lambda x: x[0]):
        for player, score in get_match_results(match)['points'].items():
            player_stats[player]['points'] += score
            player_stats[player]['matches'] += 1

        table = []
        for player in players_set:
            if player_stats[player]['matches']:
                table.append({
                    'name': player,
                    'match_count': player_stats[player]['matches'],
                    'coef': round(player_stats[player]['points'] * 100 /
                                  (player_stats[player]['matches'] * 3), 1),
                })

        table = sorted(table, key=functools.cmp_to_key(comparator))

        position = table.index({
            'name': player_name,
            'match_count': player_stats[player_name]['matches'],
            'coef': round(player_stats[player_name]['points'] * 100 /
                          (player_stats[player_name]['matches'] * 3), 1),
        }) if player_stats[player_name]['matches'] else -1

        if position != -1:
            delta_set['cur'] = {
                'below': ((players_set -
                           {player for player in players_set
                            if player_stats[player]['matches']})
                          |
                          set(player['name']
                              for player in table[position + 1:])),
                'above': set(player['name'] for player in table[:position]),
            }
            if delta_set['prev']:
                diff = {
                    'below': (delta_set['prev']['above'] &
                              delta_set['cur']['below']),
                    'above': (delta_set['prev']['below'] &
                              delta_set['cur']['above']),
                }
                result.append([date, position + 1, table[position]['coef'],
                               ', '.join(sorted(diff['below'])),
                               ', '.join(sorted(diff['above']))])
            else:
                result.append([date, position + 1, table[position]['coef'],
                               '', ''])

            delta_set['prev'] = delta_set['cur']
        else:
            result.append([date, len(players_set), '-', '', ''])

    result = [[i + 1] + elem for i, elem in enumerate(reversed(result))]

    return {'columns': 6,
            'data': result}


def calculate(matches):
    """
    The main function of the component
    """
    LOGGER.info('Calculating statistics')

    players_set = get_players_set(matches)
    response = {
        key: {} for key in players_set.union(['MAIN'])
    }

    response['MAIN']['total_points'] = get_total_points(matches)

    for player in players_set:
        response[player]['coef_history'] = (
            get_coef_history(matches, player, MIN_MATCH_COUNT))

    LOGGER.info('Statistics is successfully calculated!')

    return response
