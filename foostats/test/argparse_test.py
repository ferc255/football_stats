import unittest

from foostats.application import parse_args


class ArgparseTest(unittest.TestCase):
    def test_full_run(self):
        result = parse_args(['full-run'])
        self.assertEqual('full-run', result['action'])
        self.assertIn('/matches.json', result['src'])
        self.assertIn('/processed.json', result['dst'])

    def test_full_run_src_dst_file(self):
        self.assertDictEqual(
            {
                'action': 'full-run',
                'src': 'src_file_path',
                'dst': 'dst_file_path',
            },
            parse_args(['full-run',
                        '--src', 'src_file_path',
                        '--dst', 'dst_file_path']))

    def test_full_run_extra_arg(self):
        self.assertRaises(SystemExit, parse_args, ['full-run', '--some_arg'])

    def test_fetch_data(self):
        result = parse_args(['fetch-data'])
        self.assertEqual('fetch-data', result['action'])
        self.assertIn('/matches.json', result['dst'])

    def test_fetch_data_dst_file(self):
        self.assertDictEqual(
            {
                'action': 'fetch-data',
                'dst': 'file_path',
            },
            parse_args(['fetch-data', '--dst', 'file_path']))

    def test_fetch_data_extra_arg(self):
        self.assertRaises(SystemExit, parse_args, ['fetch-data', '--some_arg'])
        self.assertRaises(SystemExit, parse_args, ['fetch-data', '--src', 'x'])

    def test_draw(self):
        result = parse_args(['draw'])
        self.assertEqual('draw', result['action'])
        self.assertIn('/processed.json', result['src'])

    def test_draw_src_file(self):
        self.assertDictEqual(
            {
                'action': 'draw',
                'src': 'file_path',
            },
            parse_args(['draw', '--src', 'file_path']))

    def test_draw_extra_arg(self):
        self.assertRaises(SystemExit, parse_args, ['draw', '--some_arg'])
        self.assertRaises(SystemExit, parse_args, ['draw', '--dst', 'x'])

    def test_add_match(self):
        result = parse_args(['add-match'])
        self.assertEqual('add-match', result['action'])
        self.assertIn('/matches.json', result['dst'])

    def test_add_match_dst_file(self):
        self.assertDictEqual(
            {
                'action': 'add-match',
                'dst': 'file_path',
            },
            parse_args(['add-match', '--dst', 'file_path']))

    def test_add_match_extra_arg(self):
        self.assertRaises(SystemExit, parse_args, ['add-match', '--some_arg'])
        self.assertRaises(SystemExit, parse_args, ['add-match', '--src', 'x'])

    def test_compute(self):
        result = parse_args(['compute'])
        self.assertEqual('compute', result['action'])
        self.assertIn('/matches.json', result['src'])
        self.assertIn('/processed.json', result['dst'])

    def test_compute_src_dst_file(self):
        self.assertDictEqual(
            {
                'action': 'compute',
                'src': 'src_file_path',
                'dst': 'dst_file_path',
            },
            parse_args(['compute',
                        '--src', 'src_file_path',
                        '--dst', 'dst_file_path']))

    def test_compute_extra_arg(self):
        self.assertRaises(SystemExit, parse_args, ['compute', '--some_arg'])
        self.assertRaises(SystemExit, parse_args, ['compute', 'x', 'y'])

    def test_no_action_argument(self):
        self.assertRaises(SystemExit, parse_args, [])


if __name__ == '__main__':
    unittest.main()
