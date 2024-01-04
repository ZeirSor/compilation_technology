from .item import Item

from typing import List
from enum import Enum, auto


class StateType(Enum):
    INITIAL = "Initial"
    MEDIATE = "Mediate"
    FINAL = "Final"


class CanonicalItemSet:
    # 静态属性，用于生成唯一的状态编号
    status_num = 0

    object_registry = []

    def __new__(cls, grammar, start_item: List[Item]):
        # 检查对象是否已经创建过
        for insts in cls.object_registry:
            if insts.start_item_list == start_item and insts.grammar == grammar:
                return insts

        # 如果没有创建过，调用父类的 __new__ 方法创建新的实例
        instance = super(CanonicalItemSet, cls).__new__(cls)
        # 将新创建的实例添加到对象注册表中
        cls.object_registry.append(instance)
        return instance

    def __init__(self, grammar, start_item_list: List[Item], state_type=StateType.MEDIATE):
        # 通过静态属性获取唯一的状态编号
        self.seq_num = CanonicalItemSet.status_num
        # 自增状态编号，确保下一个项目集有不同的状态编号
        CanonicalItemSet.status_num += 1

        self.grammar = grammar

        # 项目集的起始项目
        self.start_item_list: List[Item] = start_item_list

        # 通过闭包算法计算项目的闭包（closure），得到项目集中包含的项目列表
        self.items: List[Item] = self.closure(start_item_list)

        self.next_symbols = self.get_next_symbols()

        # 存储在某个输入符号下，项目集转移到的下一个状态的信息
        self.next_status_set = set()
        # 键是输入符号，值是对应的项目集对象
        self.next_status_dict = {}

        self.state_type = state_type

    def closure(self, start_item_list: List[Item]):
        # 初始化闭包列表为输入的起始项目集
        closure_list = start_item_list

        # expanded标志项目集有无扩大，项目集没扩大代表算法完成，退出循环
        expanded = True
        while expanded:
            expanded = False
            # 遍历当前闭包列表中的每个项目
            for item in closure_list:
                # 检查项目是否处于待约状态（即尚未扩展）
                if item.is_pending():
                    # 获取项目点后面的符号
                    next_symbol = item.rhs[item.position + 1]
                    # 获取该符号的起始项目集
                    next_items = self.grammar.get_symbol_start_item(next_symbol)
                    # 将起始项目集中的项目添加到闭包列表，如果不在列表中则进行扩展，并设置expanded = True
                    for next_item in next_items:
                        if next_item not in closure_list:
                            closure_list.append(next_item)
                            expanded = True

        # 返回最终闭包列表
        return closure_list

    def goto(self, symbol):
        # 初始化新的项目列表
        next_item_list = []

        # 遍历当前项目集中的每个项目
        for item in self.items:
            # 如果项目是移进项目或者待约项目
            if item.is_shift() or item.is_pending():
                # 如果项目的点后面的符号等于给定的符号
                if item.rhs[item.position + 1] == symbol:
                    # 将当前项目的移进项目加入新的项目列表中
                    next_item_list.append(item.shift())

        # 根据新的项目列表创建一个新的项目集
        next_item_set = CanonicalItemSet(self.grammar, next_item_list)

        # 返回新的项目集
        return next_item_set

    def set_state_to_final(self):
        self.state_type = StateType.FINAL

    def set_state_to_initial(self):
        self.state_type = StateType.INITIAL

    def get_next_symbols(self):
        next_symbols = []

        for item in self.items:
            rhs = item.rhs
            position = item.position
            if (item.is_shift() or item.is_pending()) and rhs[position + 1] not in next_symbols:
                next_symbols.append(rhs[item.position + 1])

        return next_symbols

    def __repr__(self):
        return f"CanonicalItemSet(seq_num={self.seq_num}, items={self.items})"

    def __str__(self):
        return f"{[item for item in self.items]}"

    def __eq__(self, other):
        return self.items == other.items

    def __hash__(self):
        # 将对象的哈希值定义为对象属性的哈希值的异或操作
        return hash(self.seq_num)
