from tabulate import tabulate

from .grammar import Grammar
from .dfa import DFA
from utils.print_tools import dict_to_2d_table

from typing import Dict, List


class LR0Parser:
    def __init__(self, grammar: Grammar):
        print('构建LR(0)分析器...')
        self.grammar = grammar

        self.dfa = DFA(grammar, grammar.start_item)

        self.state_set = self.dfa.status_list
        self.action_table: Dict[int, Dict[str, List[str, int]]] = {}
        self.goto_table: Dict[int, Dict[str, int]] = {}

        self.build_parsing_table()

    def build_parsing_table(self):

        for i in range(len(self.state_set)):
            if i not in self.action_table:
                self.action_table[i] = {}
            if i not in self.goto_table:
                self.goto_table[i] = {}

        for state in self.state_set:
            if state.next_status_dict:
                for shift, next_state in state.next_status_dict.items():
                    # print(shift, next_state.seq_num)
                    if shift.islower():
                        self.action_table[state.seq_num][shift] = f"S_{next_state.seq_num}"
                    elif shift.isupper():
                        self.goto_table[state.seq_num][shift] = next_state.seq_num
            else:
                if len(state.items) > 1:
                    print('存在规约-规约冲突！！！')
                else:
                    item = state.start_item[0]
                    if item.is_reduce():
                        # print(f'reduce: {item}, {item.type}')
                        for symbol in self.grammar.terminals + ['#']:
                            self.action_table[state.seq_num][
                                symbol] = f"r_{self.grammar.productions.index(item.production)}"
                    elif item.is_accept():
                        self.action_table[state.seq_num]['#'] = "acc"

    def parse(self, input_string):
        # 初始化分析过程
        step_num = 1
        state_stack = [0]  # 状态栈
        symbol_stack = ['#']  # 符号栈
        input_buffer = list(input_string) + ['#']  # 输入缓冲区
        action = ''
        goto = ''

        each_step_dict = {
            'state stack': '',
            'symbol stack': '',
            'input buffer': '',
            'action': '',
            'goto': '',
        }
        all_step_dict: Dict[int, Dict] = {}

        def update_step_dict(state_stack, symbol_stack, input_buffer, action, goto=''):
            each_step_dict['state stack'] = ' '.join([str(x) for x in state_stack])
            each_step_dict['symbol stack'] = ''.join(symbol_stack)
            each_step_dict['input buffer'] = ''.join(input_buffer)
            each_step_dict['action'] = action
            each_step_dict['goto'] = goto

            nonlocal step_num
            all_step_dict[step_num] = each_step_dict.copy()
            step_num = step_num + 1

        while True:
            current_state = state_stack[-1]
            current_symbol = input_buffer[0]

            if current_state in self.action_table and current_symbol in self.action_table[current_state]:
                all_step_dict[step_num] = {key: '' for key in each_step_dict.keys()}

                act = self.action_table[current_state][current_symbol].split('_')
                if len(act) == 1:
                    act = act[0]
                else:
                    act, num = act
                    # print(f'step {step_num}: {act} {num}')

                if act.lower() == 's':
                    update_step_dict(state_stack, symbol_stack, input_buffer, f'{act}_{num}')

                    state_stack.append(int(num))
                    symbol_stack.append(current_symbol)
                    input_buffer.pop(0)
                elif act.lower() == 'r':
                    update_step_dict(state_stack, symbol_stack, input_buffer, f'{act}_{num}')

                    reduce_production = self.grammar.productions[int(num)]

                    k = len(reduce_production.rhs)
                    while k > 0:
                        state_stack.pop()
                        symbol_stack.pop()
                        k -= 1

                    non_terminal = reduce_production.lhs
                    next_state = self.goto_table[state_stack[-1]].get(non_terminal, None)
                    symbol_stack.append(non_terminal)
                    if next_state != None:
                        each_step_dict['goto'] = next_state
                        all_step_dict[step_num] = each_step_dict.copy()
                        state_stack.append(self.goto_table[state_stack[-1]][non_terminal])
                    else:

                        rows = list(range(1, step_num))
                        columns = each_step_dict.keys()
                        data = all_step_dict
                        dict_to_2d_table(data, rows, columns)

                        return "Error"
                elif act.lower() == 'acc':
                    update_step_dict(state_stack, symbol_stack, input_buffer, f'{act}')

                    rows = list(range(1, step_num))
                    columns = each_step_dict.keys()
                    data = all_step_dict
                    dict_to_2d_table(data, rows, columns)

                    return "Accept!"
            else:
                # 错误处理
                update_step_dict(state_stack, symbol_stack, input_buffer, 'error')

                rows = list(range(1, step_num))
                columns = each_step_dict.keys()
                data = all_step_dict
                dict_to_2d_table(data, rows, columns)

                return "Error"

    def show_action_goto_table(self):
        rows = list(range(len(self.state_set)))
        columns = self.grammar.terminals + ['#'] + self.grammar.non_terminals
        columns.remove(self.grammar.start_symbol)

        data = self.action_table
        for k, v in data.items():
            v.update(self.goto_table[k])

        dict_to_2d_table(data, rows, columns)

    def show_dfa(self):
        print("DFA:")
        for state, transitions in self.dfa.items():
            print(f"State {state}:")

    def __str__(self):
        return f"Grammar:\n{self.grammar}\nDFA:\n{self.dfa}"

    def __repr__(self):
        return f"Grammar:\n{self.grammar}\nDFA:\n{self.dfa}"
