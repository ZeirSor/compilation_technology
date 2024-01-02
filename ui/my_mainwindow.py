import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem

from core import LR0Parser
from .mainwindow import Ui_MainWindow
from utils import create_grammar
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # This initializes the UI components defined in mainwindow_ui.py

        self.grammar = None

        self.setTabStyleSheet(self.productionItem_tabWidget, 2.45)
        self.setTabStyleSheet(self.function_tabWidget, 9.85)

        # Connect signals and slots or add additional functionality as needed
        self.openFileBtn.clicked.connect(self.import_productions)
        self.runBtn.clicked.connect(self.init_LR0Parser)

        # self.action_goto_table_textEdit.setHtml(
        #     "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>HTML表格示例</title><style>table{width:100%;border-collapse:collapse;margin-top:20px}th,td{border:1px solid #dddddd;text-align:left;padding:8px}th{background-color:#f2f2f2}</style></head><body><h2>学生信息表</h2><table><thead><tr><th>学号</th><th>姓名</th><th>年龄</th><th>专业</th></tr></thead><tbody><tr><td>001</td><td>张三</td><td>20</td><td>计算机科学</td></tr><tr><td>002</td><td>李四</td><td>22</td><td>电子工程</td></tr><tr><td>003</td><td>王五</td><td>21</td><td>化学</td></tr></tbody></table></body></html>")

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
        ...

    def show_dfa_states(self):
        print('show_dfa_states')
        ...

    def show_action_goto_table(self):
        print('show_action_goto_table')
        ...

    def analyze_input(self):
        print('analyze_input')
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
