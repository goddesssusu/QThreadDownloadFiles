import json
import sys

from PyQt6.QtWidgets import QApplication

from view.tableWidget import TableWidget
from view.winUi import WinUi


class Window(WinUi):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        with open('../config/config.json', 'r') as f:
            config = json.load(f)
            print(config.get("threadCount"))
        self.tableWidget = TableWidget(threadCount=config.get("threadCount"))
        self.horizontalLayout_5.addWidget(self.tableWidget)
        self.pushButton_2.clicked.connect(
            lambda: self.tableWidget.getDownloadFileTotalSize(
                self.lineEdit.text()) if self.lineEdit.text() else None)
# https://dldir1.qq.com/qqfile/qq/PCQQ9.7.6/QQ9.7.6.28989.exe
# https://d2ae4a42c64ab864f525820ca443040a.rdt.tfogc.com:49156/dldir1.qq.com/weixin/Windows/WeChatSetup.exe

if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = Window()
    p.show()
    sys.exit(app.exec())