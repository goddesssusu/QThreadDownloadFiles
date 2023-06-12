
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QLabel, QSizePolicy, QSpacerItem, QComboBox


class WinUi(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(WinUi, self).__init__(*args, **kwargs)
        self.__setQSS()
        self.__initializeWidgets()

    def __initializeWidgets(self):
        self.resize(1400, 595)
        self.centralwidget = QWidget()
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.horizontalLayout_2 = QHBoxLayout()
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("输入下载链接")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton_2 = QPushButton("下载")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, 60, -1)
        self.horizontalLayout_4.setSpacing(6)
        self.label_5 = QLabel("当前保存路径:")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.label_4 = QLabel("")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.pushButton = QPushButton("更改")
        self.pushButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.horizontalLayout_4.addWidget(self.pushButton)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                           QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(10)
        self.label_3 = QLabel("选择下载线程数:")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBox = QComboBox()
        self.comboBox.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred))
        self.comboBox.addItems(['1', '2', '3', '4', '5', '6', '7', '8'])
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 1)
        self.setCentralWidget(self.centralwidget)

    def __setQSS(self):
        self.setStyleSheet("""
            QLabel{
                font-size:14px;
            }
            QPushButton{
                font-size:14px;
                padding: 6 20 6 20;
            }
            QLineEdit{
                font-size:14px;
                min-height:30px;
                padding-left:6;
            }
            QTableWidget::item {
                font-size:10px;
            }
            QComboBox{
                font-size:14px;
                max-width:60px;
                min-width:60px;
            }
        """)