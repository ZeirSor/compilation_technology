class ListContainer:
    # 类变量，用于跟踪已经创建的对象和对应的实例
    object_registry = []

    def __new__(cls, my_list):
        # 检查对象是否已经创建过
        for insts in cls.object_registry:
            if insts.my_list == my_list:
                return insts
        else:
            # 如果没有创建过，调用父类的 __new__ 方法创建新的实例
            instance = super(ListContainer, cls).__new__(cls)
            # 将新创建的实例添加到对象注册表中
            cls.object_registry.append(instance)
            return instance

    def __init__(self, my_list):
        # 实例变量，存储列表
        self.my_list = my_list

    def add_to_list(self, item):
        self.my_list.append(item)

    def get_list(self):
        return self.my_list

    def clear_list(self):
        self.my_list = []


# 示例用法
container1 = ListContainer([1, 2, 3])
container2 = ListContainer([1, 2, 3])
container3 = ListContainer([4, 5, 6])

print("Object 1 ID:", id(container1))  # 输出: Object 1 ID: ...
print("Object 2 ID:", id(container2))  # 输出: Object 2 ID: ...
print("Object 3 ID:", id(container3))  # 输出: Object 3 ID: ...

print(container1 is container2)  # 输出: True，因为相同的 my_list 对象返回同一实例
print(container1 is container3)  # 输出: False，因为不同的 my_list 对象返回不同实例
