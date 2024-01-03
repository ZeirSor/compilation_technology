from graphviz import Digraph
from utils.init import create_parser

lr0_parser = create_parser("./examples/example1.txt")


# # 创建有向图对象
# dot = Digraph(comment='The Round Table')
#
# # 添加节点
# dot.node('A')
# dot.node('B')
# dot.node('L')
#
# # 添加边
# dot.edges(['AB', 'AL'])


def create_graph():
    dot = Digraph(comment='The Round Table')

    for state in lr0_parser.state_set:
        dot.node(str(state.seq_num))

    for state in lr0_parser.state_set:
        if state.next_status_set:
            for symbol, next_state in state.next_status_dict.items():
                print(f"{state.seq_num}-->{next_state.seq_num}")
                dot.edge(str(state.seq_num), str(next_state.seq_num), label=symbol)
    return dot


if __name__ == '__main__':
    dot = create_graph()
    # 渲染图形并保存到文件
    dot.render('test-output/round-table.gv', view=True, format='png')
