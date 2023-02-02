import unittest
from datetime import datetime
from app.utils.calculator import DT, Calc


class TestDT(unittest.TestCase):
    '''
    How to run tests:
    python -m unittest -v tests/test_utils/test_calculator.py
    '''
    def setUp(self):
        self.dt = DT('28-05-2023 11:30')

    def test_get_datetime(self):
        # output datetime fomat: year, month, day, hour, minute
        self.assertEqual(self.dt.get_datetime(), datetime(2023, 5, 28, 11, 30))

    def test_set_datetime(self):
        test_cases = [
            {'string': '08.12.22 14:22', 'expected': [2022, 12, 8, 14, 22]},
            {'string': '12/08/22', 'expected': [2022, 8, 12, 0, 0]},
            {'string': '1.06.2021', 'expected': [2021, 6, 1, 0, 0]},
            {'string': '1-1-2022', 'expected': [2022, 1, 1, 0, 0]},
            {'string': '25/12/22 04:00', 'expected': [2022, 12, 25, 4, 0]},
            {'string': '12/25/22 04:00', 'expected': [2022, 12, 25, 4, 0]},
            {'string': '1 Jan 23', 'expected': [2023, 1, 1, 0, 0]},
            {'string': '08 June 2023', 'expected': [2023, 6, 8, 0, 0]},
            {'string': 'June 8 2023', 'expected': [2023, 6, 8, 0, 0]},
            {'string': '24 Aug 2024 20:00', 'expected': [2024, 8, 24, 20, 0]},
        ]
        for case in test_cases:
            self.dt.set_datetime(case['string'])
            self.assertEqual(self.dt.get_datetime(), datetime(*case['expected']))

    def test_str(self):
        self.assertEqual(str(self.dt), '28 May 23 11:30')
