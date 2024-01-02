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

    @classmethod
    def __get_separator(cls) -> str:
        return cls.__separator

    @classmethod
    def _set_separator(cls, new_separator: str):
        cls.__separator = new_separator

    def generation_is_empty(self):
        if self.rhs == 'ε':
            return True
        else:
            return False

    def __str__(self):
        return f"{self.lhs} {self.__get_separator()} {self.rhs}"

    def __repr__(self):
        return f"ProductionFormula({self.lhs}, {self.rhs})"

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self):
        # Ensure that the hash is based on immutable attributes
        return hash((self.lhs, self.rhs))
