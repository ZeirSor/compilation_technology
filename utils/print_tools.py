from graphviz import Digraph
from tabulate import tabulate


def dict_to_2d_table(data, rows, columns):
    table_data = [[data[row].get(col, '') for col in columns] for row in rows]
    # 将二维列表转换为表格
    table = tabulate(table_data, headers=columns, showindex=rows, tablefmt='pretty', stralign='left')
    # 打印表格
    table_html = tabulate(table_data, headers=columns, showindex=rows, tablefmt='html')
    print(table)

    return table_html


def create_graph(lr0_parser):
    dot = Digraph(comment='The Round Table')

    for state in lr0_parser.state_set:
        dot.node(str(state.seq_num))

    for state in lr0_parser.state_set:
        if state.next_status_set:
            for symbol, next_state in state.next_status_dict.items():
                print(f"{state.seq_num}-->{next_state.seq_num}")
                dot.edge(str(state.seq_num), str(next_state.seq_num), label=symbol)
    return dot
