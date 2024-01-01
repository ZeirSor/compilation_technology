from core import LR0Parser
from utils import create_grammar


def test(filepath):
    grammar = create_grammar(filepath)
    parser = LR0Parser(grammar)
    # print('start_symbol', grammar.terminals)
    # print('non_terminals', grammar.non_terminals)
    # print('start_symbol', grammar.start_symbol)
    # print(grammar.production_to_dict())
    # status_list = grammar.dfa.status_list
    # for state in status_list:
    #     print(state.seq_num, state.items, state.next_symbols)
    return parser


parser = test('./examples/example1.txt')
