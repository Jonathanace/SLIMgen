class Calculator:
    """
    A simple calculator class with add and subtract functions.
    """

    def __init__(self):
        pass

    def add(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Input values must be integers")
        return x + y

    def subtract(self, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Input values must be integers")
        return x - y