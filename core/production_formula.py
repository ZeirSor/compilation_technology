

class ProductionFormula(object):
    """
    This class is used to represent a production formula.
    """
    __separator = '->'

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.non_terminal = set(filter(str.isupper, lhs)) | set(filter(str.isupper, rhs))
        self.terminal = set(filter(str.islower, rhs))

    def __str__(self):
        return f"{self.lhs} {self.__get_separator()} {self.rhs}"

    def __repr__(self):
        return f"ProductionFormula({self.lhs}, {self.rhs})"

    @classmethod
    def __get_separator(cls) -> str:
        return cls.__separator

    @classmethod
    def _set_separator(cls, new_separator: str):
        cls.__separator = new_separator


    def gen_is_epsilon(self):
        if self.rhs == 'ε':
            return True
        else:
            return False