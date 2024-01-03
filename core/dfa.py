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
        self.states_list.append(CanonicalItemSet(self.grammar, [self.start_item]))
        self.states_list[0].set_state_to_initial()

        while True:
            expanded = False
            for state in self.states_list:
                if state.next_symbols:
                    for symbol in state.next_symbols:
                        # print(state, symbol)
                        new_state = state.goto(symbol)
                        if new_state not in self.states_list:
                            self.states_list.append(new_state)
                            expanded = True
                        else:
                            new_state.seq_num = self.states_list.index(new_state)
                            state.next_status_set.add(new_state)
                            state.next_status_dict[symbol] = new_state
            if not expanded:
                break

        for state in self.states_list:
            if not state.next_symbols:
                state.set_state_to_final()

        print("DFA.build_transitions")
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
