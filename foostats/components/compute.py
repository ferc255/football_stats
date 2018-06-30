"""
Processes the set of games and returns statistics in json format, which
should be displayed in Google Spreadsheets in the future.
"""
import json
import sys
import collections


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
    for player, score in sorted(total_points.items(), key=lambda x: -x[1]):
        result.append([player, score])
    return result


def calculate(matches):
    """
    The main function of the component
    """
    response = {
        'MAIN': {},
    }
    response['MAIN']['total_points'] = get_total_points(matches)

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
