from .item import Item
from typing import List


class CanonicalItemSet:
    # 静态属性，用于生成唯一的状态编号
    status_num = 0

    object_registry = []

    def __new__(cls, grammar, start_item: List[Item]):
        # 检查对象是否已经创建过
        for insts in cls.object_registry:
            if insts.start_item == start_item and insts.grammar == grammar:
                return insts

        # 如果没有创建过，调用父类的 __new__ 方法创建新的实例
        instance = super(CanonicalItemSet, cls).__new__(cls)
        # 将新创建的实例添加到对象注册表中
        cls.object_registry.append(instance)
        return instance

    def __init__(self, grammar, start_item: List[Item]):
        # 通过静态属性获取唯一的状态编号
        self.seq_num = CanonicalItemSet.status_num
        # 自增状态编号，确保下一个项目集有不同的状态编号
        CanonicalItemSet.status_num += 1

        self.grammar = grammar

        # 项目集的起始项目
        self.start_item: List[Item] = start_item

        # 通过闭包算法计算项目的闭包（closure），得到项目集中包含的项目列表
        self.items: List[Item] = self.closure(start_item)

        self.next_symbols = self.get_next_symbols()

        # 存储在某个输入符号下，项目集转移到的下一个状态的信息
        self.next_status_set = set()
        # 键是输入符号，值是对应的项目集对象
        self.next_status_dict = {}

    def closure(self, start_item: List[Item]):
        closure_list = start_item

        expanded = True
        while expanded:
            expanded = False

            for item in closure_list:
                if item.is_pending():
                    next_symbol = item.rhs[item.position + 1]
                    next_items = self.grammar.get_symbol_start_item(next_symbol)

                    for next_item in next_items:
                        if next_item not in closure_list:
                            closure_list.append(next_item)
                            expanded = True

        return closure_list

    def goto(self, symbol):
        """
        计算下一个项目集，其中当前项目集中的项目都是形如A -> alpha B beta的形式，
        且beta的第一个符号是符号symbol。
        """
        next_item_list = []

        for item in self.items:
            if item.rhs[item.position + 1] == symbol:
                # 移除箭头，将项目加入新的项目集中
                next_item_list.append(item.shift())

        next_item_set = CanonicalItemSet(self.grammar, next_item_list)

        return next_item_set

    def get_next_symbols(self):
        next_symbols = []

        for item in self.items:
            rhs = item.rhs
            position = item.position
            if (item.is_shift() or item.is_pending()) and rhs[position + 1] not in next_symbols:
                next_symbols.append(rhs[item.position + 1])

        return next_symbols

    def __repr__(self):
        return f"CanonicalItemSet(start_item={self.start_item}, items={self.items})"

    def __str__(self):
        return f"{[item for item in self.items]}"

    def __eq__(self, other):
        return self.seq_num == other.seq_num

    def __hash__(self):
        return hash(self.seq_num)
