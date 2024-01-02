from .production_formula import ProductionFormula

from enum import Enum, auto


class ItemType(Enum):
    SHIFT = "Shift Item"
    PENDING = "Pending Item"
    REDUCE = "Reduce Item"
    ACCEPT = "Accept Item"


class Item(object):
    object_registry = []

    def __new__(cls, production: ProductionFormula, position: int):
        # 检查对象是否已经创建过
        for insts in cls.object_registry:
            if insts.production == production and insts.position == position:
                return insts

        # 如果没有创建过，调用父类的 __new__ 方法创建新的实例
        instance = super(Item, cls).__new__(cls)
        # 将新创建的实例添加到对象注册表中
        cls.object_registry.append(instance)
        return instance

    def __init__(self, production: ProductionFormula, position: int):

        self.production = production

        try:
            if position < 0:
                raise ValueError("Negative position. position is corrected to 0.")
            elif position > len(self.production.rhs):
                raise ValueError("Position exceeds length of production. position is corrected to len(rhs)")
        except ValueError as e:
            print(f"Warning: {e}")
            position = max(0, min(position, len(self.production.rhs)))

        self.position = position
        self.lhs = self.production.lhs

        # 先将字符串转化为字符列表，再将·插入列表，再转化回字符串
        rhs_list = list(self.production.rhs)
        rhs_list.insert(position, '·')
        self.rhs = ''.join(rhs_list)
        if self.production.generation_is_empty():
            self.rhs = '·'
        # self.judge_item_type()

    def shift(self):
        if self.position != len(self.rhs) - 1:
            return Item(self.production, self.position + 1)
        return self

    def judge_item_type(self) -> ItemType:
        if self.position == len(self.rhs) - 1:
            return ItemType.REDUCE
        elif self.rhs[self.position + 1] in self.production.terminal:
            return ItemType.SHIFT
        elif self.rhs[self.position + 1] in self.production.non_terminal:
            return ItemType.PENDING

    def is_reduce(self) -> bool:
        return self.type == ItemType.REDUCE

    def is_shift(self) -> bool:
        return self.type == ItemType.SHIFT

    def is_pending(self) -> bool:
        return self.type == ItemType.PENDING

    def is_accept(self) -> bool:
        return self.type == ItemType.ACCEPT

    def is_start(self):
        return self.position == 0

    def __str__(self):
        return f"{self.lhs} -> {self.rhs}"

    def __repr__(self):
        return f"Item({self.lhs}, {self.rhs})"

    def __eq__(self, other):
        return self.lhs == other.lhs and \
               self.rhs == other.rhs and \
               self.position == other.position and \
               self.type == other.type and \
               self.production == other.production

    def __hash__(self):
        # Ensure that the hash is based on immutable attributes
        return hash((self.lhs, self.rhs, self.position, self.type, self.production))
