import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(self.calculator.add(1, 2), 3)
        with self.assertRaises(ValueError):
            self.calculator.add("a", "b")

    def test_subtract(self):
        self.assertEqual(self.calculator.subtract(2, 1), 1)
        with self.assertRaises(ValueError):
            self.calculator.subtract("a", "b")