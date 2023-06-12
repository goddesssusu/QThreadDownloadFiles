import sys

from PyQt6.QtWidgets import QApplication, QTableWidget, QPushButton
from threads.getTotalSize import GetTotalSize
from threads.subDownloadFile import SubDownloadFile
from view.progressBar import ProgressBar
from view.timeManagementContainer import TimeManagementContainer


class TableWidget(QTableWidget):

    def __init__(self, threadCount, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)

        # 创建表格
        self._threadCount = threadCount
        self.setColumnCount(7 + threadCount)
        self.setHorizontalHeaderLabels(
            ["操作", "文件名", "大小", "状态", "剩余时间", "传输速度"] +
            ["线程{}".format(i + 1) for i in range(threadCount)])
        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._getTotalSizeThd = GetTotalSize(parent=self)
        # self._getTotalSizeThd.totalSize.connect(self.__creatSubDownloadFileThread)
        self._getTotalSizeThd.totalSize.connect(self.__addRow)
        self._timeManagementContainers = []

    def getDownloadFileTotalSize(self, url: str):
        self._getTotalSizeThd.url = url
        self._getTotalSizeThd.start()

    def __creatSubDownloadFileThread(self, totalSize, url):
        # 计算每个线程下载的数据块范围
        block_size = totalSize // self._threadCount
        for i in range(self._threadCount):
            startByte = i * block_size
            endByte = startByte + block_size - 1 if i < self._threadCount - 1 else totalSize - 1
            thread = SubDownloadFile(index=i, url=url, startByte=startByte, endByte=endByte)
            thread.downloadProgress.connect(self.updateProgress)
            thread.start()

    def __addRow(self, totalSize, url):
        row_count = self.rowCount()
        self.insertRow(row_count)
        timeManagementContainer = TimeManagementContainer(
            threadCount=self._threadCount, totalSize=totalSize, url=url, parent=self)
        timeManagementContainer.start(1000)

        self.setCellWidget(row_count, 0, timeManagementContainer.button)
        self.setItem(row_count, 1, timeManagementContainer.fileNameItem)
        self.setItem(row_count, 2, timeManagementContainer.totalSizeItem)
        self.setItem(row_count, 3, timeManagementContainer.stateItem)
        self.setItem(row_count, 4, timeManagementContainer.remainingTimeItem)
        self.setItem(row_count, 5, timeManagementContainer.downloadSpeedItem)

        for i, progressBar in enumerate(timeManagementContainer.progressBarContainer):
            self.setCellWidget(row_count, i + 6, progressBar)


    def updateProgress(self, row, column, value):
        progress = self.cellWidget(row, column)
        if progress is not None and isinstance(progress, ProgressBar):
            progress.setValue(value)
