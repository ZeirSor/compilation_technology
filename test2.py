from graphviz import Digraph

dot = Digraph(comment='这是一个有向图')
dot.node('A', '作者', fontname="Heiti")
dot.node('B', '医生')
dot.node('C', '律师')
dot.edges(['AB', 'AC'])
dot.edge('B', 'C')
dot.format = 'png'

dot.render('test-output/round-table.gv', view=True, format='png')
