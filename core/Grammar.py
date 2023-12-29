from .production_formula import ProductionFormula
from .item import Item, ItemType

class Grammar(object):
    def __init__(self, productions: list, name='test_grammar'):
        self.name = name
        self.productions = productions

        self.__set_non_terminals()
        self.__set_terminals()

        self.start_symbol = self.productions[0].lhs
        self.items = self.gen_items()


    def gen_items(self):
        item_list = []

        count = 0
        for production in self.productions:
            for position in range(len(production.rhs) + 1):
                item = Item(production, position)
                if production.gen_is_epsilon():
                    break
                if count == 0 and item.is_reduce():
                    item.item_type = ItemType.ACCEPT

                item_list.append(item)
                count = count + 1
            ...

        print(item_list)

        return item_list

    @property
    def non_terminals(self):
        return self.__non_terminals

    # 计算非终结符集
    def __set_non_terminals(self):
        non_terminals = set()
        for production in self.productions:
            assert isinstance(production, ProductionFormula)
            non_terminals.add(production.lhs)

        self.__non_terminals = list(non_terminals)


    @property
    def terminals(self):
        return self.__terminals

    # 计算终结符集
    def __set_terminals(self):
        terminals = set()
        for production in self.productions:
            assert isinstance(production, ProductionFormula)
            for symbol in production.rhs:
                if not self.is_non_terminal(symbol):
                    terminals.add(symbol)

        self.__terminals = list(terminals)


    def __repr__(self):
        return f"<Grammar name: {self.name}, productions: {self.productions}>"

    def to_dict(self):
        production_dict = {}

        for production in self.productions:
            if production.lhs not in production_dict:
                production_dict[production.lhs] = []

            production_dict[production.lhs].append(production.rhs)

        return production_dict

    def add_production(self, production: ProductionFormula):
        self.productions.append(production)

    def first(self, x):
        ...

    def follow(self, x):
        ...

    def is_non_terminal(self, x):
        if x in self.non_terminals:
            return True
        else:
            return False

    def is_terminal(self, x):
        if x in self.terminals:
            return True
        else:
            return False

    # @classmethod
    # def gen_is_epsilon(cls, x: ProductionFormula):
    #     if x.rhs == 'ε':
    #         return True
    #     ...


