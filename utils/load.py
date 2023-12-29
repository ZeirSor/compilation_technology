from core import ProductionFormula, Grammar, Item


def get_productions(filepath: str) -> list:
    productions = []

    with open(filepath, encoding='utf-8', mode='r') as f:
        for line in f:
            lhs, rhs = line.strip().split('->')
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
    grammar = create_grammar('../examples/example1.txt')
    print(grammar.terminals)
    print(grammar.non_terminals)
    print(grammar.start_symbol)
    print(grammar.to_dict())

    for i in grammar.items:
        print(i, i.type)
    # s = 'sadfADF'
    # sep = '·'
    # lst = list(s)
    # lst.insert(1, sep)
    # print(lst)
    # print(''.join(lst))


