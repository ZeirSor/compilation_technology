from .production_formula import ProductionFormula
from .item import Item, ItemType

from typing import List, Dict


class Grammar(object):
    def __init__(self, productions: list, name='test_grammar'):
        self.name = name
        self.productions = productions

        self.__set_non_terminals()
        self.__set_terminals()

        self.start_symbol: str = self.productions[0].lhs
        self.items: List[Item] = self.gen_all_items()
        self.start_item = self.items[0]

        self.production_dict = self.production_to_dict()
        self.item_dict = self.item_to_dict()

    def gen_all_items(self):
        item_list = []  # Initialize an empty list to store the generated items

        count = 0
        for production in self.productions:  # Iterate over all productions in the grammar
            for position in range(
                    len(production.rhs) + 1):  # Iterate over all positions in the right-hand side of the production, including the end position
                item = Item(production, position)  # Create a new item object with the current production and position

                # Handle special cases for empty productions and accept item
                if production.generation_is_empty():  # If the production generates the empty string
                    break  # Skip generating additional items
                item.type = item.judge_item_type()  # Determine the type of the item

                # The specification project is a special case of accepting the project. Mark the first specification project of the expansion project as accepted.
                if count == 0 and item.is_reduce():  # If it is the first production and the item is a reduce item
                    item.type = ItemType.ACCEPT  # Set the item type to accept

                item_list.append(item)  # Append the generated item to the item list
            count = count + 1

        return item_list  # Return the generated item list

    def get_symbol_start_item(self, lhs):
        start_item_list = []
        for item in self.item_dict[lhs]:
            if item.is_start():
                start_item_list.append(item)

        return start_item_list

    def item_to_dict(self):
        item_dict = {}

        for item in self.items:
            if item.lhs not in item_dict:
                item_dict[item.lhs] = []

            item_dict[item.lhs].append(item)

        return item_dict

    def production_to_dict(self):
        production_dict = {}

        for production in self.productions:
            if production.lhs not in production_dict:
                production_dict[production.lhs] = []

            production_dict[production.lhs].append(production)

        return production_dict

    # --------------------------------------------
    # ---------------计算非终结符集-----------------
    # --------------------------------------------
    def __set_non_terminals(self):
        non_terminals = set()
        for production in self.productions:
            assert isinstance(production, ProductionFormula)
            non_terminals.add(production.lhs)

        self.__non_terminals = list(non_terminals)

    @property
    def non_terminals(self):
        return self.__non_terminals

    def is_non_terminal(self, x):
        if x in self.non_terminals:
            return True
        else:
            return False

    # --------------------------------------------
    # -----------------计算终结符集-----------------
    # --------------------------------------------
    @property
    def terminals(self):
        return self.__terminals

    #
    def __set_terminals(self):
        terminals = set()
        for production in self.productions:
            assert isinstance(production, ProductionFormula)
            for symbol in production.rhs:
                if not self.is_non_terminal(symbol):
                    terminals.add(symbol)

        self.__terminals = list(terminals)

    def is_terminal(self, x):
        if x in self.terminals:
            return True
        else:
            return False

    # --------------------------------------------
    # --------------------------------------------
    # --------------------------------------------

    def __str__(self):
        return f"Grammar: {self.name}\n\nProductions:\n{self.productions}"

    def __repr__(self):
        return f"<Grammar name: {self.name}, productions: {self.productions}>"
