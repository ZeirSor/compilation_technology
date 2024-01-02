from core import ProductionFormula, Grammar


def get_productions(filepath: str) -> list:
    productions = []

    with open(filepath, encoding='utf-8', mode='r') as f:
        for line in f:
            line = line.replace(' ', '')
            if '|' not in line:
                lhs, rhs = line.strip().split('->')
                productions.append(ProductionFormula(lhs, rhs))
            else:
                lhs, rhs_list = line.strip().split('->')
                for rhs in rhs_list.split('|'):
                    productions.append(ProductionFormula(lhs, rhs))
    # 扩展文法
    start_symbol = productions[0].__str__()[0]
    start_lhs = start_symbol + '\''
    start_rhs = start_symbol
    productions.insert(0, ProductionFormula(start_lhs, start_rhs))

    return productions


def create_grammar(filepath: str):
    productions = get_productions(filepath)
    grammar = Grammar(productions)

    return grammar


if __name__ == '__main__':
    # grammar = create_grammar('../examples/example1.txt')
    # print(grammar.terminals)
    # print(grammar.non_terminals)
    # print(grammar.start_symbol)
    # print(grammar.production_to_dict())
    #
    # print('------------------------------------------------------------------------------------------')

    grammar2 = create_grammar('../examples/example2.txt')
    print(grammar2.terminals)
    print(grammar2.non_terminals)
    print(grammar2.start_symbol)
    print(grammar2.production_to_dict())

    print('------------------------------------------------------------------------------------------')

    # grammar3 = create_grammar('../examples/example3.txt')
    # print(grammar3.terminals)
    # print(grammar3.non_terminals)
    # print(grammar3.start_symbol)
    # print(grammar3.production_to_dict())
    # dfa = DFA(grammar, grammar.items[0])
    # init_itemset = CanonicalItemSet(grammar, grammar.items[0])
    # for i in grammar.items:
    #     print(i, i.type)
    # s = 'sadfADF'
    # sep = '·'
    # lst = list(s)
    # lst.insert(1, sep)
    # print(lst)
    # print(''.join(lst))
