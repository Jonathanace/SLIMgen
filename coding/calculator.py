# calculator.py
class Calculator:
    """A simple calculator for performing arithmetic operations."""

    def add(self, num1: float, num2: float) -> float:
        """Adds two numbers together and returns the result."""
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            raise TypeError("Arguments must be of type int or float.")
        return num1 + num2

    def subtract(self, num1: float, num2: float) -> float:
        """Subtracts two numbers and returns the result."""
        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            raise TypeError("Arguments must be of type int or float.")
        return num1 - num2