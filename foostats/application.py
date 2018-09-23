import argparse
import os
import sys
import json

from foostats.settings import BASE_DIR
from foostats.components.fetch_data import fetch_data
from foostats.components.compute import calculate
from foostats.components.ui import draw


def parse_args(args):
    action_parser = argparse.ArgumentParser('foostats')
    action_parser.add_argument(
        'action',
        choices=['full-run', 'fetch-data', 'compute', 'draw', 'add-match'],
    )
    result = {
        'action': action_parser.parse_args([args[0]]).action
    }

    database_dir = os.path.join(BASE_DIR, 'database')

    def update_parser_args(result, action, pairs, args):
        parser = argparse.ArgumentParser('foostats ' + action)
        for pair in pairs:
            parser.add_argument('--' + pair[0],
                                default=os.path.join(database_dir,
                                                     pair[1]))
        parser = parser.parse_args(args)
        for pair in pairs:
            result[pair[0]] = getattr(parser, pair[0])

    if result['action'] == 'fetch-data':
        update_parser_args(
            result,
            'fetch-data',
            [('dst', 'matches.json')],
            args[1:],
        )
    elif result['action'] == 'compute':
        update_parser_args(
            result,
            'compute',
            [('src', 'matches.json'),
             ('dst', 'processed.json')],
            args[1:],
        )
    elif result['action'] == 'draw':
        update_parser_args(
            result,
            'draw',
            [('src', 'processed.json')],
            args[1:],
        )
    elif result['action'] == 'add-match':
        update_parser_args(
            result,
            'add-match',
            [('dst', 'matches.json')],
            args[1:],
        )
    elif result['action'] == 'full-run':
        update_parser_args(
            result,
            'full-run',
            [('src', 'matches.json'),
             ('dst', 'processed.json')],
            args[1:],
        )

    return result


def load_json(filename):
    return json.load(open(filename))


def dump_json(data, filename):
    json.dump(data, open(filename, 'w+'), indent=2, ensure_ascii=False)


def handle_fetch_data(dst):
    matches = fetch_data()
    dump_json(matches, dst)


def handle_compute(src, dst):
    matches = load_json(src)
    data = calculate(matches)
    dump_json(data, dst)


def handle_draw(src):
    data = load_json(src)
    draw(data)


def app():
    args = parse_args(sys.argv[1:])

    for end in ['src', 'dst']:
        if args.get(end) is not None:
            os.makedirs(os.path.dirname(args[end]), exist_ok=True)

    if args['action'] == 'fetch-data':
        handle_fetch_data(args['dst'])
    elif args['action'] == 'compute':
        handle_compute(args['src'], args['dst'])
    elif args['action'] == 'draw':
        handle_draw(args['src'])
    elif args['action'] == 'add-match':
        pass
    elif args['action'] == 'full-run':
        handle_fetch_data(args['src'])
        handle_compute(args['src'], args['dst'])
        handle_draw(args['dst'])
