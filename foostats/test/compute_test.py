"""
Testing the middle stage
"""
import unittest
from foostats.components import compute


class ProcessMatchesTest(unittest.TestCase):
    """
    Match processing
    """
    def setUp(self):
        """
        Initial actions before each test
        """
        self.data = {
            "2018.06.01": {
                "score": [15, 10],
                "red": ["Алексей", "Герман", "Андрей"],
                "green": [],
                "blue": ["Саша", "Дима", "Виталий"]
            },
            "2018.06.02": {
                "score": [9, 9],
                "red": ["Герман", "Дима", "Виталий"],
                "green": [],
                "blue": ["Саша", "Алексей", "Андрей"]
            },
            "2018.06.03": {
                "score": [3, 1, 0],
                "red": ["Дима", "Андрей"],
                "green": ["Виталий", "Алексей"],
                "blue": ["Герман", "Саша"]
            }
        }

    def test_total_points(self):
        """
        Calculate total points
        """
        response = compute.calculate(self.data)['MAIN']['total_points']

        self.assertEqual([['Андрей', 7],
                          ['Алексей', 5],
                          ['Герман', 4],
                          ['Дима', 4],
                          ['Виталий', 2],
                          ['Саша', 1]],
                         response['data'])
        self.assertEqual(2, response['columns'])

    def test_points_history(self):
        """
        Calculate points history
        """
        response = compute.calculate(self.data)
        self.assertEqual([["2018.06.01", 0, 5],
                          ["2018.06.02", 1, 5],
                          ["2018.06.03", 4, 4]],
                         response['Дима']['points_history']['data'])
        self.assertEqual([["2018.06.01", 0, 4],
                          ["2018.06.02", 1, 4],
                          ["2018.06.03", 2, 5]],
                         response['Виталий']['points_history']['data'])

        self.assertEqual(3, response['Саша']['points_history']['columns'])


if __name__ == '__main__':
    unittest.main()
