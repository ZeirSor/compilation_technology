from .item import Item
from .canonical_item_set import CanonicalItemSet
from .grammar import Grammar

from typing import List


class DFA(object):
    def __init__(self, grammar, start_item: Item):
        self.grammar: Grammar = grammar
        self.start_item = start_item

        self.status_list: List[CanonicalItemSet] = []
        self.build_transitions()

    # 计算状态集的闭包

    def build_transitions(self):
        self.status_list.append(CanonicalItemSet(self.grammar, [self.start_item]))

        while True:
            expanded = False
            for state in self.status_list:
                if state.next_symbols:
                    for symbol in state.next_symbols:
                        new_state = state.goto(symbol)
                        if new_state not in self.status_list:
                            self.status_list.append(new_state)
                            expanded = True
                        else:
                            new_state.seq_num = self.status_list.index(new_state)
                            state.next_status_set.add(new_state)
                            state.next_status_dict[symbol] = new_state

            if not expanded:
                break

        print("DFA.build_transitions")
        return self.status_list

    def print_dfa(self):
        for i in range(len(self.status_list)):
            state = self.status_list[i]
            print(state.seq_num, state)
            for k, v in state.next_status_dict.items():
                print(f"    {state.seq_num}---{k}--->{v.seq_num} {v}")
            print('------------------------------------------------')

    def __str__(self):
        return f"DFA({self.start_item}, {self.status_list})"

    def __repr__(self):
        return f"DFA({self.start_item}, {self.status_list})"
