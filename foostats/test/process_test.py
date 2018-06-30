"""
Testing the middle stage
"""
import unittest
from foostats.components import compute


class ProcessMatchesTest(unittest.TestCase):
    """
    Match processing
    """
    def test_total_points(self):
        """
        Calculate total points
        """
        data = {
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
        response = compute.calculate(data)['MAIN']['total_points']

        self.assertCountEqual([['Андрей', 7],
                               ['Алексей', 5],
                               ['Герман', 4],
                               ['Дима', 4],
                               ['Виталий', 2],
                               ['Саша', 1]],
                              response)


if __name__ == '__main__':
    unittest.main()
