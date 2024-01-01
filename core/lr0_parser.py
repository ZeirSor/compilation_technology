from .grammar import Grammar
from .dfa import DFA


class LR0Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

        self.dfa = DFA(grammar, grammar.start_item)

        self.state_set = self.dfa.status_list
        self.action_table = {}
        self.goto_table = {}

    def build_parsing_table(self):
        # 构建LR(0)分析表
        pass

    def parse(self, input_string):
        # 初始化分析过程
        state_stack = [0]  # 状态栈
        symbol_stack = ['#']  # 符号栈
        input_buffer = list(input_string) + ['#']  # 输入缓冲区

        while True:
            current_state = state_stack[-1]
            current_symbol = input_buffer[0]

            # 根据当前状态和输入符号查找分析表
            if current_state in self.action_goto_table and current_symbol in self.action_goto_table[current_state]:
                action = self.action_goto_table[current_state][current_symbol]

                if action[0] == 'shift':
                    # 移入操作
                    state_stack.append(action[1])
                    symbol_stack.append(current_symbol)
                    input_buffer = input_buffer[1:]
                elif action[0] == 'reduce':
                    # 规约操作
                    production = action[1]
                    num_to_pop = len(production.rhs)
                    state_stack = state_stack[:-num_to_pop]
                    symbol_stack = symbol_stack[:-num_to_pop]

                    # 更新状态和符号栈
                    state_stack.append(self.goto(state_stack[-1], production.lhs))
                    symbol_stack.append(production.lhs)
                elif action[0] == 'accept':
                    # 接受操作
                    return "Accept"
            else:
                # 错误处理
                return "Error"

    def goto(self, state, symbol):
        # 根据LR(0)自动机的状态转移规则计算新状态
        pass

    def __str__(self):
        return f"Grammar:\n{self.grammar}\nDFA:\n{self.dfa}"

    def __repr__(self):
        return f"Grammar:\n{self.grammar}\nDFA:\n{self.dfa}"

