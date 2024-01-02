from tabulate import tabulate


def dict_to_2d_table(data, rows, columns):
    table_data = [[data[row].get(col, '') for col in columns] for row in rows]
    # 将二维列表转换为表格
    table = tabulate(table_data, headers=columns, showindex=rows, tablefmt='pretty', stralign='left')
    # 打印表格
    table_html = tabulate(table_data, headers=columns, showindex=rows, tablefmt='html')
    print(table)

    return table_html
