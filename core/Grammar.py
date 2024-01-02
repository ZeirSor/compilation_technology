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
        item_list = []

        count = 0
        for production in self.productions:
            for position in range(len(production.rhs) + 1):
                item = Item(production, position)

                # 空产生式只会有一个项目
                if production.generation_is_empty():
                    break
                # 规约项目是接受项目的特殊情况，将拓展项目的第一个规约项目其标记为接受
                item.type = item.judge_item_type()

                if count == 0 and item.is_reduce():
                    item.type = ItemType.ACCEPT

                item_list.append(item)
            count = count + 1

        return item_list

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
