"""
Testing the middle stage
"""
import unittest
import json
import os

from foostats.components import compute
from foostats.test import module


class ProcessMatchesTest(unittest.TestCase):
    """
    Match processing
    """
    def setUp(self):
        """
        Initial actions before each test
        """
        self.min_file, self.min_data = self.open_test_json('min_test.json')
        self.middle_file, self.middle_data = self.open_test_json(
            'middle_test.json')

    def tearDown(self):
        self.min_file.close()
        self.middle_file.close()

    @staticmethod
    def open_test_json(testname):
        file = open(
            os.path.join(
                os.path.dirname(__file__),
                os.path.join('test_artifacts', testname))
        )
        data = json.load(file)
        return file, data

    def test_calculate_completeness(self):
        players_set = compute.get_players_set(self.middle_data)

        response = compute.calculate(self.middle_data)

        self.assertCountEqual(['MAIN'] + list(players_set),
                              response.keys())
        for player in players_set:
            self.assertCountEqual(
                module.PLAYER_STATS,
                response[player].keys())

    def test_total_points(self):
        """
        Calculate total points
        """
        response = compute.get_total_points(self.min_data)

        self.assertEqual([['Андрей', 7],
                          ['Алексей', 5],
                          ['Герман', 4],
                          ['Дима', 4],
                          ['Виталий', 2],
                          ['Саша', 1]],
                         response['data'])
        self.assertEqual(2, response['columns'])

    def test_coef_history(self):
        """
        Calculate points history
        """
        self.assertEqual([[1, '2018.06.05', 5, 25.0, '', 'Сергей'],
                          [2, '2018.06.04', 4, 25.0, '', ''],
                          [3, '2018.06.03', 4, 22.2, '', 'Дима'],
                          [4, '2018.06.02', 3, 16.7, '', ''],
                          [5, '2018.06.01', 3, 0.0, '', '']],
                         compute.get_coef_history(
                             self.middle_data, 'Виталий', 2)['data'])

        self.assertEqual([[1, '2018.06.05', 6, 22.2, '', 'Сергей'],
                          [2, '2018.06.04', 5, 16.7, '', ''],
                          [3, '2018.06.03', 5, 16.7, 'Саша', 'Дима'],
                          [4, '2018.06.02', 5, 33.3, '', ''],
                          [5, '2018.06.01', 8, '-', '', '']],
                         compute.get_coef_history(
                             self.middle_data, 'Герман', 2)['data'])

        self.assertEqual([[1, '2018.06.05', 2, 77.8, '', ''],
                          [2, '2018.06.04', 2, 77.8,
                           'Алексей, Виталий, Саша', ''],
                          [3, '2018.06.03', 5, 66.7,
                           'Герман', 'Виталий, Саша'],
                          [4, '2018.06.02', 4, 33.3, '', ''],
                          [5, '2018.06.01', 8, '-', '', '']],
                         compute.get_coef_history(
                             self.middle_data, 'Дима', 3)['data'])

        self.assertEqual(
            6,
            compute.get_coef_history(
                self.middle_data, 'Максим', 5)['columns']
        )


if __name__ == '__main__':
    unittest.main()
