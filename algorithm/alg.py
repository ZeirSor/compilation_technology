from core import Grammar, Item, CanonicalItemSet
from typing import List, Tuple, Set

# def separate_terminals_and_non_terminals(input_string: str) -> Tuple[Set[str], Set[str]]:
#     """
#     将输入字符串中的大写字母视为非终结符，小写字母视为终结符，分别放入两个集合中。
#     """
#     terminals = set(filter(str.islower, input_string))
#     non_terminals = set(filter(str.isupper, input_string))
#
#     return terminals, non_terminals


# 计算状态集的闭包
# generated_items = []  # 存放已生成的项目
# processing_items = start_item  # 存放已处理的项目
#
# while processing_items:
#     current_item = processing_items.pop(0)  # 取出一个待处理的项目
#
#     if current_item.is_pending() and current_item not in generated_items:
#         # 待约项目会需要继续添加lhs为对应非终结符的所有项目
#         next_lhs = current_item.rhs[current_item.position + 1]
#         next_productions = grammar.production_dict[next_lhs]
#
#         for production in next_productions:
#             processing_items.append(Item(production, 0))
#
#     generated_items.append(current_item)
#
# return generated_items

# def closure(grammar: Grammar, start_item: List[Item]):
#     closure_list = start_item
#
#     expanded = True
#     while expanded:
#         expanded = False
#
#         for item in closure_list:
#             if item.is_pending():
#                 next_symbol = item.rhs[item.position + 1]
#                 next_items = grammar.get_symbol_start_item(next_symbol)
#
#                 for next_item in next_items:
#                     if next_item not in closure_list:
#                         closure_list.append(next_item)
#                         expanded = True
#
#     return closure_list

# def goto(grammar, current_item_set: CanonicalItemSet, symbol, status_list):
#     """
#     计算下一个项目集，其中当前项目集中的项目都是形如A -> alpha B beta的形式，
#     且beta的第一个符号是符号symbol。
#     """
#     next_item_list = []
#
#     for item in current_item_set.items:
#         if item.rhs[item.position + 1] == symbol:
#             # 移除箭头，将项目加入新的项目集中
#             next_item_list.append(item.shift())
#
#     next_item_set = CanonicalItemSet(grammar, next_item_list, status_list)
#
#     return next_item_set
