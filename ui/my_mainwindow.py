import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QVBoxLayout, QGridLayout, QLabel, \
    QListWidget, QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QSizePolicy

from core import LR0Parser
from .mainwindow import Ui_MainWindow
from utils import create_grammar
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # This initializes the UI components defined in mainwindow_ui.py

        self.openFileBtn.setEnabled(True)
        self.runBtn.setEnabled(False)

        self.grammar = None

        self.setTabStyleSheet(self.productionItem_tabWidget, 2.45)
        self.setTabStyleSheet(self.function_tabWidget, 9.85)

        # Connect signals and slots or add additional functionality as needed
        self.openFileBtn.clicked.connect(self.import_productions)
        self.runBtn.clicked.connect(self.init_LR0Parser)
        self.start_analyze_pushButton.clicked.connect(self.analyze_input)

    def insert_item_set(self):
        # 创建网格布局
        grid_layout = QGridLayout(self.item_set_widget)

        n = len(self.lr0_parser.state_set)
        num1, num2 = self.find_closest_numbers(n)
        # 初始化一个数据列表
        data_list = ["Item 1", "Item 2", "Item 3"]

        print(num1, num2)

        count = 0
        # 循环遍历网格，为每个单元格创建有边框的小部件，其中包含编号标签和无边框的QListWidget
        for i in range(num1):
            for j in range(num2):
                # 创建有边框的小部件
                cell_widget = QWidget()
                cell_widget.setStyleSheet("border: 1px solid black;")

                cell_layout = QVBoxLayout(cell_widget)

                if count < n:
                    # 插入编号标签
                    print(i, j, n)
                    label = QLabel(f'State {count} -- {self.lr0_parser.state_set[count].state_type.value}')
                    label.setStyleSheet("border: none;")
                    label.setFont(QFont("Arial", 15, QFont.Bold))  # 设置黑体、加粗、字号大一点
                    cell_layout.addWidget(label)

                    # 插入 QListWidget，并去掉边框
                    list_widget = QListWidget()
                    list_widget.setStyleSheet("border: none;")  # 去掉QListWidget的边框
                    list_widget.setSelectionMode(QListWidget.NoSelection)

                    for item in self.lr0_parser.state_set[count].items:
                        list_item = QListWidgetItem(item.__str__())
                        list_item.setFont(QFont("Arial", 13))
                        list_item.setToolTip(item.__repr__())
                        list_widget.addItem(list_item)

                    cell_layout.addWidget(list_widget)

                    # 将小部件插入到网格中
                    grid_layout.addWidget(cell_widget, i, j)
                    count = count + 1

        # 设置网格布局到 item_set_widget
        self.item_set_widget.setLayout(grid_layout)

    def insert_action_goto_table(self):

        action_size = len(self.lr0_parser.grammar.terminals) + 1
        goto_size = len(self.lr0_parser.grammar.non_terminals) - 1
        states_num = len(self.lr0_parser.state_set)

        self.action_goto_horizontalLayout.setStretch(0, 1)
        self.action_goto_horizontalLayout.setStretch(1, action_size)
        self.action_goto_horizontalLayout.setStretch(2, goto_size)
        self.action_goto_title_horizontalLayout.setStretch(0, 1)
        self.action_goto_title_horizontalLayout.setStretch(1, action_size)
        self.action_goto_title_horizontalLayout.setStretch(2, goto_size)

        self.insert_state_num_table(states_num)
        self.insert_action_table(states_num)
        self.insert_goto_table(states_num)

        self.states_num_tableWidget.setStyleSheet("QTableWidget { border: none; }")
        self.action_tableWidget.setStyleSheet("QTableWidget { border: none; }")
        self.goto_tableWidget.setStyleSheet("QTableWidget { border: none; }")
        self.analyze_tableWidget.setStyleSheet("QTableWidget { border: none; }")
        ...

    def insert_state_num_table(self, states_num):
        self.states_num_tableWidget.setRowCount(states_num)
        self.states_num_tableWidget.setColumnCount(1)

        font = QFont("Times New Roman", 15)
        # font.setItalic(True)
        font.setBold(True)
        # self.analyze_tableWidget.verticalHeader().setFont(font)
        self.analyze_tableWidget.horizontalHeader().setFont(font)

        # 插入列编号，从1到10
        for i in range(states_num):
            item = QTableWidgetItem(str(i))
            self.states_num_tableWidget.setItem(i, 0, item)
            font = QFont("Times New Roman", 12)
            # font.setItalic(True)
            # font.setBold(True)
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)

        # 设置其他表格内容...
        # self.states_num_tableWidget.setItem(row, col, QTableWidgetItem("Your Data"))
        self.states_num_tableWidget.setHorizontalHeaderLabels(["状态编号"])
        self.states_num_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.states_num_tableWidget.setAlternatingRowColors(True)
        self.states_num_tableWidget.verticalHeader().hide()
        # self.states_num_tableWidget.verticalHeader().ResizeMode(QHeaderView.Stretch)

        header = self.states_num_tableWidget.verticalHeader()
        for i in range(states_num):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        # header = self.states_num_tableWidget.horizontalHeader()
        # for i in range(states_num):
        #     header.setSectionResizeMode(i, QHeaderView.Stretch)

        # 设置表格的大小策略为 Expanding
        # self.states_num_tableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.states_num_tableWidget.resizeColumnToContents()
        # self.states_num_tableWidget.resizeRowToContents()

    def insert_action_table(self, states_num):
        self.action_tableWidget.setRowCount(states_num)

        col_headers = sorted(self.lr0_parser.grammar.terminals) + ['#']
        self.action_tableWidget.setColumnCount(len(col_headers))
        print(col_headers)

        self.action_tableWidget.setVerticalHeaderLabels([str(x) for x in list(range(states_num))])
        self.action_tableWidget.setHorizontalHeaderLabels(col_headers)
        self.action_tableWidget.verticalHeader().hide()

        font = QFont("Times New Roman", 15)
        # font.setItalic(True)
        font.setBold(True)
        # self.analyze_tableWidget.verticalHeader().setFont(font)
        self.action_tableWidget.horizontalHeader().setFont(font)

        dict = self.lr0_parser.action_table
        for i in range(states_num):
            for j in col_headers:
                item = QTableWidgetItem((dict[i].get(j, '')))
                font = QFont("Times New Roman", 12)
                font.setItalic(True)
                font.setBold(True)
                item.setFont(font)
                self.action_tableWidget.setItem(i, col_headers.index(j), item)
                item.setTextAlignment(Qt.AlignCenter)

        #
        # # 设置其他表格内容...
        # # self.states_num_tableWidget.setItem(row, col, QTableWidgetItem("Your Data"))
        # self.states_num_tableWidget.setHorizontalHeaderLabels(["状态编号"])
        self.action_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.action_tableWidget.setAlternatingRowColors(True)

        header = self.action_tableWidget.verticalHeader()
        for i in range(states_num):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        header = self.action_tableWidget.horizontalHeader()
        for i in range(len(col_headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        # header = self.action_tableWidget.horizontalHeader()
        # for i in range(states_num):
        #     header.setSectionResizeMode(i, QHeaderView.Stretch)

    def insert_goto_table(self, states_num):
        self.goto_tableWidget.setRowCount(states_num)

        col_headers = sorted(self.lr0_parser.grammar.non_terminals)
        col_headers.remove(self.lr0_parser.grammar.start_symbol)
        self.goto_tableWidget.setColumnCount(len(col_headers))
        print(len(col_headers))

        self.goto_tableWidget.setVerticalHeaderLabels([str(x) for x in list(range(states_num))])
        self.goto_tableWidget.setHorizontalHeaderLabels(col_headers)
        self.goto_tableWidget.verticalHeader().hide()

        font = QFont("Times New Roman", 15)
        # font.setItalic(True)
        font.setBold(True)
        # self.analyze_tableWidget.verticalHeader().setFont(font)
        self.goto_tableWidget.horizontalHeader().setFont(font)

        dict = self.lr0_parser.goto_table
        for i in range(states_num):
            for j in col_headers:
                print(j)
                item = QTableWidgetItem(str((dict[i].get(j, ''))))
                font = QFont("Times New Roman", 12)
                font.setItalic(True)
                font.setBold(True)
                item.setFont(font)
                self.goto_tableWidget.setItem(i, col_headers.index(j), item)
                item.setTextAlignment(Qt.AlignCenter)

        #
        # # 设置其他表格内容...
        # # self.states_num_tableWidget.setItem(row, col, QTableWidgetItem("Your Data"))
        # self.states_num_tableWidget.setHorizontalHeaderLabels(["状态编号"])
        self.goto_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.goto_tableWidget.setAlternatingRowColors(True)

        header = self.goto_tableWidget.verticalHeader()
        for i in range(states_num):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        header = self.goto_tableWidget.horizontalHeader()
        for i in range(len(col_headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def init_LR0Parser(self):
        print('按钮2被点击')
        self.openFileBtn.setEnabled(True)
        self.runBtn.setEnabled(False)

        self.lr0_parser = LR0Parser(self.grammar)

        self.lr0_parser.show_action_goto_table()
        self.lr0_parser.parse('bccd')

        self.show_CanonicalItemSet()
        self.show_dfa_states()
        self.show_action_goto_table()

    def show_CanonicalItemSet(self):
        print('show_CanonicalItemSet')
        self.insert_item_set()
        ...

    def show_dfa_states(self):
        print('show_dfa_states')
        ...

    def show_action_goto_table(self):
        print('show_action_goto_table')
        self.insert_action_goto_table()
        ...

    def analyze_input(self):
        print('analyze_input')

        input_str = self.inputString_lineEdit.text()
        self.lr0_parser.parse(input_str)

        print(self.lr0_parser.all_step_dict.keys())
        print(self.lr0_parser.each_step_dict.keys())

        # self.action_tableWidget.setRowCount(states_num)

        row_headers = [str(x) for x in list(self.lr0_parser.all_step_dict.keys())]
        self.analyze_tableWidget.setRowCount(len(row_headers))
        print(row_headers)

        col_headers = list(self.lr0_parser.each_step_dict.keys())
        self.analyze_tableWidget.setColumnCount(len(col_headers))
        print(col_headers)

        font = QFont("Times New Roman", 15)
        # font.setItalic(True)
        font.setBold(True)
        self.analyze_tableWidget.verticalHeader().setFont(font)
        self.analyze_tableWidget.horizontalHeader().setFont(font)
        #
        self.analyze_tableWidget.setVerticalHeaderLabels(row_headers)
        self.analyze_tableWidget.setHorizontalHeaderLabels(col_headers)

        dict = self.lr0_parser.all_step_dict
        for i in range(1, len(row_headers) + 1):
            for j in col_headers:
                item = QTableWidgetItem(str(dict[i].get(j, '')))
                font = QFont("Times New Roman", 12)
                font.setItalic(True)
                font.setBold(True)
                item.setFont(font)
                self.analyze_tableWidget.setItem(i - 1, col_headers.index(j), item)
                item.setTextAlignment(Qt.AlignCenter)

        self.analyze_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.analyze_tableWidget.setAlternatingRowColors(True)
        #
        header = self.analyze_tableWidget.verticalHeader()
        for i in range(len(row_headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        header = self.analyze_tableWidget.horizontalHeader()
        for i in range(len(col_headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        ...

    def set_grammar(self, grammar):
        self.grammar = grammar

    def setTabStyleSheet(self, tabWidget, size):
        width = tabWidget.width()
        tabCount = tabWidget.count()
        tabWidth = width / tabCount * size
        print(tabWidget, tabCount, tabWidth, width)
        tabWidget.setStyleSheet(f"QTabBar::tab{{width:{tabWidth}%;}}")

    def import_productions(self):
        self.openFileBtn.setEnabled(False)
        self.runBtn.setEnabled(True)

        self.production_listWidget.clear()
        self.item_listWidget.clear()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # 打开文件对话框
        abs_file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Text Files (*.txt);;All Files (*)",
                                                       options=options)
        file_name = os.path.basename(abs_file_path)

        print("File Name:", abs_file_path)

        self.fileNameLineEdit_.setText(file_name)

        if abs_file_path:
            print(f'Selected File: {abs_file_path}')

        self.set_grammar(create_grammar(abs_file_path))

        for i in range(len(self.grammar.productions)):
            lwItem = QListWidgetItem()
            lwItem.setText(f"  ({i + 1})\t{self.grammar.productions[i].__str__()}")
            lwItem.setToolTip(f"{self.grammar.productions[i].__repr__()}")
            self.production_listWidget.addItem(lwItem)

        for i in range(len(self.grammar.items)):
            lwItem = QListWidgetItem()
            lwItem.setText(f"  ({i + 1})\t{self.grammar.items[i].__str__()}")
            lwItem.setToolTip(f"{self.grammar.items[i].__repr__()}")
            self.item_listWidget.addItem(lwItem)
        # print(grammar)

    def find_closest_numbers(self, n):
        sqrt_n = int(n ** 0.5)  # 求n的平方根并取整
        num1 = sqrt_n
        num2 = sqrt_n - 1

        while num1 * num2 <= n:
            # print(num1, num2)
            num1 += 1
            num2 += 1

        return num1, num2
