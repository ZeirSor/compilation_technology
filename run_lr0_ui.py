import sys

from PyQt5.QtWidgets import QApplication

from ui.my_mainwindow import MyMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
