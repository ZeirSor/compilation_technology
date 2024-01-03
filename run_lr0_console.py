from core import LR0Parser
from utils.init import create_parser

if __name__ == '__main__':
    parser = create_parser('./examples/example1.txt')
    assert isinstance(parser, LR0Parser)

    print(parser.grammar.productions)
    print(parser.state_set)
    print(parser.dfa.print_dfa())
    print(parser.show_action_goto_table())
    print(parser.parse('bccd'))
