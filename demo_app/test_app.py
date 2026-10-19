import unittest

from app import calculate_total


class TestCalculateTotal(unittest.TestCase):
    def test_total_for_multiple_items(self):
        self.assertEqual(calculate_total(100, 3), 300)

    def test_total_for_single_item(self):
        self.assertEqual(calculate_total(100, 1), 100)

    def test_total_for_zero_quantity(self):
        self.assertEqual(calculate_total(100, 0), 0)


if __name__ == "__main__":
    unittest.main()