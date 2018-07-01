"""
Processes the set of games and returns statistics in json format, which
should be displayed in Google Spreadsheets in the future.
"""
import json
import sys
import collections


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


def get_total_points(matches):
    """
    Calculates everything so far
    """
    total_points = collections.defaultdict(int)
    for match in matches.values():
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
                total_points[player] += points_to_add[color]

    result = []
    for player, score in sorted(total_points.items(),
                                key=lambda x: (-x[1], x[0])):
        result.append([player, score])
    return result


def get_points_history(matches, player_name):
    """
    Calculates history of points for certain player
    """
    total_points = collections.defaultdict(int)
    result = []
    for date, match in sorted(matches.items(), key=lambda x: x[0]):
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
                total_points[player] += points_to_add[color]

        table = sorted(total_points.items(), key=lambda x: (-x[1], x[0]))
        position = table.index((player_name, total_points[player_name])) + 1

        result.append([date, total_points[player_name], position])

    return result


def calculate(matches):
    """
    The main function of the component
    """
    players_set = get_players_set(matches)
    response = {
        key: {} for key in players_set.union(['MAIN'])
    }

    response['MAIN']['total_points'] = get_total_points(matches)
    for player in players_set:
        response[player]['points_history'] = (
            get_points_history(matches, player))

    return response


def parse_args():
    """
    Turns input file names into dicts.
    Saves the result in file.

    Valid request:
        python3 components/compute.py \
        test/test_artifacts/min_test.json database/processed.json
    """
    json.dump(
        calculate(
            json.load(open(sys.argv[1]))
        ),
        open(sys.argv[2], 'w'),
        indent=2,
        ensure_ascii=False
    )


if __name__ == '__main__':
    parse_args()
