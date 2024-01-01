from core import LR0Parser
from utils import create_grammar
from typing import Dict, List


def test(filepath):
    grammar = create_grammar(filepath)
    lr0_parser = LR0Parser(grammar)

    # print('non_terminals', grammar.non_terminals)
    # print('start_symbol', grammar.start_symbol)
    # print(grammar.production_to_dict())
    # status_list = grammar.dfa.status_list
    # for state in status_list:
    #     print(state.seq_num, state.items, state.next_symbols)
    return lr0_parser
    # return grammar


parser = test('./examples/example2.txt')

parser.parse('abbcde')

# print(lr0_parser)
