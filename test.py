from core import LR0Parser
from utils import create_grammar
from typing import Dict, List


def test(filepath):
    grammar = create_grammar(filepath)
    lr0_parser = LR0Parser(grammar)
    return lr0_parser


parser = test('./examples/example5.txt')
assert isinstance(parser, LR0Parser)

print(parser.grammar.productions)
print(parser.state_set)
print(parser.dfa.print_dfa())
print(parser.show_action_goto_table())
print(parser.parse('bccd'))
