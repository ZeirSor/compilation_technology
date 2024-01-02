import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView


class StudentTable(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('学生信息表')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        # 创建表格
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['学号', '姓名', '年龄', '专业'])

        # 添加数据
        data = [
            ['001', '张三', '20', '计算机科学'],
            ['002', '李四', '22', '电子工程'],
            ['003', '王五', '21', '化学']
        ]

        self.table.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                item_widget = QTableWidgetItem(item)
                item_widget.setTextAlignment(5)  # 将文本居中对齐
                self.table.setItem(i, j, item_widget)

        # 合并单元格
        self.table.setSpan(0, 3, 2, 1)  # 从(0,3)到(1,3)的单元格合并

        # 设置表格属性
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列伸缩

        # 使用QSS为表格添加样式
        style = """
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f2f2f2;
                border: 1px solid #d4d4d4;
            }

            QTableWidget::item {
                padding: 8px;
            }

            QHeaderView::section {
                background-color: #e0e0e0;
                border: 1px solid #d4d4d4;
                padding: 5px;
                font-size: 14px;
            }
        """

        self.table.setStyleSheet(style)

        # 将表格添加到布局
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.table)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentTable()
    window.show()
    sys.exit(app.exec_())
