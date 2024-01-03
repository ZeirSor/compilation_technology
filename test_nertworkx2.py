import networkx as nx
import matplotlib.pyplot as plt
from utils.init import create_parser
from typing import List, Dict
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

lr0_parser = create_parser("./examples/example1.txt")


# 创建一个有向图

def create_graph():
    G = nx.DiGraph()

    for state in lr0_parser.state_set:
        G.add_node(str(state.seq_num))

    for state in lr0_parser.state_set:
        if state.next_status_set:
            for next_state in state.next_status_set:
                print(f"{state.seq_num}-->{next_state.seq_num}")
                G.add_edge(str(state.seq_num), str(next_state.seq_num))

    edge_labels: Dict[List[str, str], str] = {}
    for state in lr0_parser.state_set:
        if state.next_status_set:
            for symbol, next_state in state.next_status_dict.items():
                print(f"{state.seq_num}--{symbol}->{next_state.seq_num}")
                edge_labels[(str(state.seq_num), str(next_state.seq_num))] = symbol
                # G.add_edge(str(state.seq_num), str(next_state.seq_num))

    return G, edge_labels


if __name__ == '__main__':
    G, edge_labels = create_graph()

    print(edge_labels)

    # T = nx.balanced_tree(2, 5)
    # 绘制图形
    pos = nx.shell_layout(G)  # 定义节点位置
    nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, arrows=True)

    # 添加边上的文字
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    # 显示图形
    plt.axis("off")
    plt.show()
# 绘制图形
# pos = nx.spring_layout(G)  # 定义节点位置
# nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, arrows=True)

# 添加边上的文字
# edge_labels = {("A", "B"): "a"}  # 指定边上的标签
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

# 显示图形
# plt.axis("off")
# plt.show()


# import random
#
#
# def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
#     '''
#     From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
#     Licensed under Creative Commons Attribution-Share Alike
#
#     If the graph is a tree this will return the positions to plot this in a
#     hierarchical layout.
#
#     G: the graph (must be a tree)
#
#     root: the root node of current branch
#     - if the tree is directed and this is not given,
#       the root will be found and used
#     - if the tree is directed and this is given, then
#       the positions will be just for the descendants of this node.
#     - if the tree is undirected and not given,
#       then a random choice will be used.
#
#     width: horizontal space allocated for this branch - avoids overlap with other branches
#
#     vert_gap: gap between levels of hierarchy
#
#     vert_loc: vertical location of root
#
#     xcenter: horizontal location of root
#     '''
#     if not nx.is_tree(G):
#         raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')
#
#     if root is None:
#         if isinstance(G, nx.DiGraph):
#             root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
#         else:
#             root = random.choice(list(G.nodes))
#
#     def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
#         '''
#         see hierarchy_pos docstring for most arguments
#
#         pos: a dict saying where all nodes go if they have been assigned
#         parent: parent of this branch. - only affects it if non-directed
#
#         '''
#
#         if pos is None:
#             pos = {root: (xcenter, vert_loc)}
#         else:
#             pos[root] = (xcenter, vert_loc)
#         children = list(G.neighbors(root))
#         if not isinstance(G, nx.DiGraph) and parent is not None:
#             children.remove(parent)
#         if len(children) != 0:
#             dx = width / len(children)
#             nextx = xcenter - width / 2 - dx / 2
#             for child in children:
#                 nextx += dx
#                 pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
#                                      vert_loc=vert_loc - vert_gap, xcenter=nextx,
#                                      pos=pos, parent=root)
#         return pos
#
#     return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
