from .production_formula import ProductionFormula

from enum import Enum, auto


class ItemType(Enum):
    SHIFT = "Shift Item"
    PENDING = "Pending Item"
    REDUCE = "Reduce Item"
    ACCEPT = "Accept Item"


class Item(object):
    object_registry = []  # Registry to keep track of created instances

    def __new__(cls, production: ProductionFormula, position: int):
        # Check if the object has already been created
        for inst in cls.object_registry:
            if inst.production == production and inst.position == position:
                return inst

        # If the object hasn't been created, call the parent class's __new__ method to create a new instance
        instance = super(Item, cls).__new__(cls)
        # Add the newly created instance to the object registry
        cls.object_registry.append(instance)
        return instance

    def __init__(self, production: ProductionFormula, position: int):
        self.production = production
        self.position = position
        self.lhs = self.production.lhs

        try:
            if position < 0:
                raise ValueError("Negative position. position is corrected to 0.")
            elif position > len(self.production.rhs):
                raise ValueError("Position exceeds length of production. position is corrected to len(rhs)")
        except ValueError as e:
            print(f"Warning: {e}")
            position = max(0, min(position, len(self.production.rhs)))

        # Insert the · symbol at the specified position in the right-hand side (rhs) string
        rhs_list = list(self.production.rhs)
        rhs_list.insert(position, '·')
        self.rhs = ''.join(rhs_list)

        # If the production's generation is empty, set rhs to ·
        if self.production.generation_is_empty():
            self.rhs = '·'

    def shift(self):
        # Create a new item by shifting the position by 1, if possible
        if self.position != len(self.rhs) - 1:
            return Item(self.production, self.position + 1)
        return self

    def judge_item_type(self) -> ItemType:
        # Determine the item type based on the position and the character following · in the rhs
        if self.position == len(self.rhs) - 1:
            return ItemType.REDUCE
        elif self.rhs[self.position + 1] in self.production.terminal:
            return ItemType.SHIFT
        elif self.rhs[self.position + 1] in self.production.non_terminal:
            return ItemType.PENDING

    def is_reduce(self) -> bool:
        return self.type == ItemType.REDUCE

    def is_shift(self) -> bool:
        return self.type == ItemType.SHIFT

    def is_pending(self) -> bool:
        return self.type == ItemType.PENDING

    def is_accept(self) -> bool:
        return self.type == ItemType.ACCEPT

    def is_start(self):
        return self.position == 0

    def __str__(self):
        return f"{self.lhs} -> {self.rhs}"

    def __repr__(self):
        return f"Item({self.lhs}, {self.rhs})"

    def __eq__(self, other):
        return self.lhs == other.lhs and \
               self.rhs == other.rhs and \
               self.position == other.position and \
               self.type == other.type and \
               self.production == other.production

    def __hash__(self):
        # Ensure that the hash is based on immutable attributes
        return hash((self.lhs, self.rhs, self.position, self.type, self.production))
