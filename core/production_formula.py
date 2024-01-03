class ProductionFormula(object):
    """
    This class is used to represent a production formula.
    """

    __separator = '->'  # Separator used to separate the left-hand side (lhs) and right-hand side (rhs) of the formula

    def __init__(self, lhs, rhs):
        self.lhs = lhs  # Left-hand side of the production formula
        self.rhs = rhs  # Right-hand side of the production formula
        self.non_terminal = set(filter(str.isupper, lhs)) | set(
            filter(str.isupper, rhs))  # Set of non-terminal symbols in the formula
        self.terminal = set(filter(lambda x: not x.isupper(), rhs))  # Set of terminal symbols in the formula

    @classmethod
    def __get_separator(cls) -> str:
        return cls.__separator

    @classmethod
    def _set_separator(cls, new_separator: str):
        cls.__separator = new_separator

    def generation_is_empty(self):
        # Check if the right-hand side of the formula is equal to 'ε' (empty)
        return self.rhs == 'ε'

    def __str__(self):
        return f"{self.lhs} {self.__get_separator()} {self.rhs}"

    def __repr__(self):
        return f"ProductionFormula({self.lhs}, {self.rhs})"

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self):
        # Ensure that the hash is based on immutable attributes
        return hash((self.lhs, self.rhs))
