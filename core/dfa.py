from .item import Item
from .canonical_item_set import CanonicalItemSet
from .grammar import Grammar

from typing import List


class DFA(object):
    def __init__(self, grammar, start_item: Item):
        self.grammar: Grammar = grammar
        self.start_item = start_item

        self.states_list: List[CanonicalItemSet] = []
        self.build_transitions()

    def get_initial_state(self):
        return self.states_list[0]

    def build_transitions(self):
        # 初始化状态列表，将初始项目集加入列表，并标记为初始状态
        self.states_list.append(CanonicalItemSet(self.grammar, [self.start_item]))
        self.states_list[0].set_state_to_initial()

        # expanded标志是否有状态扩展，若有则继续循环，直到没有状态扩展为止
        expanded = True
        while expanded:
            expanded = False
            # 遍历当前状态列表中的每个状态
            for state in self.states_list:
                # 如果当前状态有可用的下一个符号
                if state.next_symbols:
                    # 遍历该状态的下一个符号
                    for symbol in state.next_symbols:
                        # 获取通过该符号进行状态转移后的新状态
                        new_state = state.goto(symbol)
                        # 如果新状态不在状态列表中，将其加入列表，并标记为扩展
                        if new_state not in self.states_list:
                            self.states_list.append(new_state)
                            expanded = True
                        else:
                            # 如果新状态已存在，设置新状态的序号并更新当前状态的下一个状态集合和字典
                            new_state.seq_num = self.states_list.index(new_state)
                            state.next_status_set.add(new_state)
                            state.next_status_dict[symbol] = new_state

        # 遍历状态列表，标记没有下一个符号的状态为终止状态
        for state in self.states_list:
            if not state.next_symbols:
                state.set_state_to_final()

        # 打印提示信息
        print("DFA.build_transitions")
        # 返回构建好的状态列表
        return self.states_list

    def print_dfa(self):
        for i in range(len(self.states_list)):
            state = self.states_list[i]
            print(state.seq_num, state, state.state_type.value)
            for k, v in state.next_status_dict.items():
                print(f"    {state.seq_num}---{k}-->{v.seq_num}\t{v}")
            print('------------------------------------------------')

    def __str__(self):
        return f"DFA({self.start_item}, {self.states_list})"

    def __repr__(self):
        return f"DFA({self.start_item}, {self.states_list})"
