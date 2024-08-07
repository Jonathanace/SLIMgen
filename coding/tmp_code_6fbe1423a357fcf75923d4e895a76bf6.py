class Calculator:
    def __init__(self):
        self.add_func = lambda x, y: x + y
        self.subtract_func = lambda x, y: x - y
    
    def set_add_func(self, add_func):
        self.add_func = add_func
    
    def set_subtract_func(self, subtract_func):
        self.subtract_func = subtract_func
    
    def get_add_func(self):
        return self.add_func
    
    def get_subtract_func(self):
        return self.subtract_func
    
    def calculate(self, func_name, x, y):
        if func_name == "add":
            return self.add_func(x, y)
        elif func_name == "subtract":
            return self.subtract_func(x, y)
    
    def reset(self):
        self.__init__()
    
    def to_string(self):
        return f"Add Function: {self.add_func}\nSubtract Function: {self.subtract_func}"