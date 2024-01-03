import networkx as nx
import matplotlib.pyplot as plt

# 创建一个有向图
G = nx.DiGraph()

# 添加节点
G.add_node("A")
G.add_node("B")
G.add_node("C")

# 添加边连接节点
G.add_edge("A", "B")
G.add_edge("B", "C")
G.add_edge("C", "A")

# 绘制图形
pos = nx.spring_layout(G)  # 定义节点位置
nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, arrows=True)

# 添加边上的文字
edge_labels = {("A", "B"): "a"}  # 指定边上的标签
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

# 显示图形
plt.axis("off")
plt.show()
