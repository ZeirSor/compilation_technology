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

        self.state_set = self.dfa.states_list
        self.action_table: Dict[int, Dict[str, List[str, int]]] = {}
        self.goto_table: Dict[int, Dict[str, int]] = {}

        self.conflict_msg = None
        self.build_parsing_table()

    def build_parsing_table(self):
        # 初始化动作表和GOTO表，确保每个状态都有对应的表项
        for i in range(len(self.state_set)):
            self.action_table[i] = {}
            self.goto_table[i] = {}

        # 遍历每个状态集合
        for state in self.state_set:
            # 如果当前状态有下一个状态
            if state.next_status_dict:
                # 遍历状态的下一个状态字典，其中键为移进的符号，值为下一个状态
                for shift_symbol, next_state in state.next_status_dict.items():
                    # 如果移进的符号是终结符
                    if not shift_symbol.isupper():
                        # 在动作表中记录移进项
                        self.action_table[state.seq_num][shift_symbol] = f"S_{next_state.seq_num}"
                    # 如果移进的符号是非终结符
                    elif shift_symbol.isupper():
                        # 在GOTO表中记录下一个状态
                        self.goto_table[state.seq_num][shift_symbol] = next_state.seq_num
            else:  # 如果状态没有下一个状态，说明是规约或接受项
                # 项目集中存在冲突
                if len(state.items) > 1:
                    conflict_msg = f"状态{state.seq_num} {state.__str__()}存在冲突！"
                    # 存在归约项冲突
                    print(state, '存在冲突')
                    reduce_num = len([item for item in state.items if item.is_reduce() or item.is_accept()])
                    shift_num = len(state.items) - reduce_num

                    if reduce_num > 1:
                        print(f'规约-规约冲突：存在{reduce_num}个归约项')
                        conflict_msg = conflict_msg + '\n' + f"规约-规约冲突：存在{reduce_num}个归约项"
                    if shift_num and shift_num:
                        print(f'移进-规约冲突：存在{shift_num}个移进项, {reduce_num}个归约项')
                        conflict_msg = conflict_msg + '\n' + f"移进-规约冲突：存在{shift_num}个移进项, {reduce_num}个归约项"

                    self.conflict_msg = conflict_msg
                else:
                    # 只有一个项目，可能是规约或接受项
                    item = state.start_item_list[0]
                    if item.is_reduce():
                        # 归约项，记录在动作表中
                        for symbol in self.grammar.terminals + ['#']:
                            self.action_table[state.seq_num][
                                symbol] = f"r_{self.grammar.productions.index(item.production)}"
                    elif item.is_accept():
                        # 接受项，记录在动作表中
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

        def update_step_dict(step_num, state_stack, symbol_stack, input_buffer, action, goto=''):
            each_step_dict['state stack'] = ' '.join([str(x) for x in state_stack])
            each_step_dict['symbol stack'] = ''.join(symbol_stack)
            each_step_dict['input buffer'] = ''.join(input_buffer)
            each_step_dict['action'] = action
            each_step_dict['goto'] = goto

            # nonlocal step_num
            all_step_dict[step_num] = each_step_dict.copy()
            # step_num = step_num + 1

        while True:
            current_state = state_stack[-1]
            current_symbol = input_buffer[0]

            # 检查动作表中是否存在对应项
            if current_state in self.action_table and current_symbol in self.action_table[current_state]:
                all_step_dict[step_num] = {key: '' for key in each_step_dict.keys()}
                each_goto = None

                # 解析动作表中的内容
                act = self.action_table[current_state][current_symbol].split('_')
                if len(act) == 1:
                    act = act[0]
                else:
                    act, num = act
                if act.lower() == 's':
                    # 移进操作
                    update_step_dict(step_num, state_stack, symbol_stack, input_buffer, f'{act}_{num}')
                    self.handle_shift(state_stack, symbol_stack, input_buffer, num)
                    step_num = step_num + 1
                elif act.lower() == 'r':
                    # 规约操作
                    update_step_dict(step_num, state_stack, symbol_stack, input_buffer, f'{act}_{num}')
                    res = self.handle_reduce(state_stack, symbol_stack, input_buffer, num, each_step_dict)

                    each_goto = each_step_dict['goto']
                    all_step_dict[step_num]['goto'] = each_goto
                    step_num = step_num + 1

                    if res == "Error":
                        # 处理规约可能的错误情况
                        self.show_parsing_table(step_num, step_num, each_step_dict, all_step_dict)
                        self.each_step_dict = each_step_dict
                        self.all_step_dict = all_step_dict
                        return "Error"
                elif act.lower() == 'acc':
                    # 接受操作
                    update_step_dict(step_num, state_stack, symbol_stack, input_buffer, f'{act}')
                    self.show_parsing_table(step_num, each_step_dict, all_step_dict)
                    self.each_step_dict = each_step_dict
                    self.all_step_dict = all_step_dict
                    return "Accept"
            else:
                # 处理无法匹配动作的情况
                update_step_dict(step_num, state_stack, symbol_stack, input_buffer, 'error')
                self.show_parsing_table(step_num, each_step_dict, all_step_dict)
                self.each_step_dict = each_step_dict
                self.all_step_dict = all_step_dict
                return "Error"

    def handle_shift(self, state_stack, symbol_stack, input_buffer, num):
        # 处理shift操作的逻辑
        state_stack.append(int(num))  # 将新的状态压入状态栈
        symbol_stack.append(input_buffer[0])  # 将当前输入符号压入符号栈
        input_buffer.pop(0)  # 从输入缓冲区中移除当前符号

    def handle_reduce(self, state_stack, symbol_stack, input_buffer, num, each_step_dict):
        # 处理reduce操作的逻辑

        reduce_production = self.grammar.productions[int(num)]  # 获取归约所用的产生式

        k = len(reduce_production.rhs)
        while k > 0:
            state_stack.pop()  # 从状态栈中弹出k个状态
            symbol_stack.pop()  # 从符号栈中弹出k个符号
            k -= 1

        non_terminal = reduce_production.lhs  # 获取产生式的左侧非终结符
        symbol_stack.append(non_terminal)  # 将左侧非终结符压入符号栈

        next_state = self.goto_table[state_stack[-1]].get(non_terminal, None)  # 获取下一个状态
        if next_state is not None:
            each_step_dict['goto'] = next_state  # 更新当前步骤的Goto信息
            state_stack.append(self.goto_table[state_stack[-1]][non_terminal])  # 将下一个状态压入状态栈
        else:
            return "Error"  # 如果下一个状态不存在，则返回错误

    def show_action_goto_table(self):
        rows = list(range(len(self.state_set)))
        columns = sorted(self.grammar.terminals) + ['#'] + sorted(self.grammar.non_terminals)
        columns.remove(self.grammar.start_symbol)

        data = self.action_table
        for k, v in data.items():
            v.update(self.goto_table[k])

        dict_to_2d_table(data, rows, columns)

    def show_parsing_table(self, step_num, each_step_dict, all_step_dict):
        rows = list(range(1, step_num + 1))
        columns = each_step_dict.keys()
        data = all_step_dict
        return dict_to_2d_table(data, rows, columns)

    def __str__(self):
        return f"Grammar:\n{self.grammar}\nDFA:\n{self.dfa}"

    def __repr__(self):
        return f"Grammar:\n{self.grammar}\nDFA:\n{self.dfa}"
