import math
import time

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QTableWidgetItem, QPushButton

from view.progressBar import ProgressBar


class TimeManagementContainer(QTimer):

    def __init__(self, threadCount, totalSize, url, *args, **kwargs):
        super(TimeManagementContainer, self).__init__(*args, **kwargs)
        self._threadCount = threadCount
        self._totalSize = totalSize
        self._url = url
        self.progressBarContainer = []
        self._formatStr = "{:.0f}%"  # 显示格式
        self._lastValue = 0  # 记录上一次下载的字节数
        self._lastTime = time.time()  # 记录上一次统计下载字节数时的时间
        self.__creatTableWidgetItem()
        self.__creatSubDownloadFileThread()
        self.timeout.connect(self.__calculateDownloadProgress)

    def __creatSubDownloadFileThread(self):
        # 计算每个线程下载的数据块范围
        blockSize = math.ceil(self._totalSize / self._threadCount)
        startByte, endByte = 0, -1
        for i in range(self._threadCount):
            endByte = min(startByte + blockSize - 1, self._totalSize - 1)
            progressBar = ProgressBar(index=i, url=self._url, startByte=startByte, endByte=endByte)
            self.progressBarContainer.append(progressBar)
            startByte = endByte + 1

    @staticmethod
    def __calculateRemainingTime(totalBytes, currentBytes, downloadSpeed):
        """计算剩余时间"""
        remainingBytes = totalBytes - currentBytes
        remainingTime = remainingBytes / downloadSpeed if downloadSpeed != 0 else 0
        return remainingTime

    @staticmethod
    def __calculateDownloadSpeed(currentBytes, previousBytes, elapsedTime):
        """计算下载速度"""
        downloadSpeed = (currentBytes - previousBytes) / elapsedTime
        return downloadSpeed

    @staticmethod
    def __calculateDownloadPercentage(downloadedBytes, totalBytes):
        """计算下载百分比"""
        downloadPercentage = (downloadedBytes / totalBytes) * 100
        return downloadPercentage

    @staticmethod
    def __convertSizeToString(sizeInBytes):
        """计算下载大小"""
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        size = sizeInBytes
        unitIndex = 0
        while size >= 1024 and unitIndex < len(units) - 1:
            size /= 1024
            unitIndex += 1
        return f"{size:.2f} {units[unitIndex]}"

    @staticmethod
    def __convertSecondsToHms(seconds):
        # 计算小时、分钟和秒数
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        # 返回时分秒格式的字符串
        if hours > 0:
            return f"{hours}小时{minutes}分钟{seconds}秒"
        elif minutes > 0:
            return f"{minutes}分钟{seconds}秒"
        else:
            return f"{seconds}秒"

    def __creatTableWidgetItem(self):
        self.fileNameItem = QTableWidgetItem(f"{self._url.split('/')[-1]}")
        self.totalSizeItem = QTableWidgetItem(self.__convertSizeToString(self._totalSize))
        self.stateItem = QTableWidgetItem()
        self.remainingTimeItem = QTableWidgetItem()
        self.downloadSpeedItem = QTableWidgetItem()
        self.button = QPushButton("暂停")
        self.button.clicked.connect(self.__operateAllThread)

    def __operateAllThread(self):
        if self.button.text() == "暂停":
            self.button.setText("继续")
            for progressBar in self.progressBarContainer:
                progressBar.pause()
        elif self.button.text() == "继续":
            self.button.setText('暂停')
            for progressBar in self.progressBarContainer:
                progressBar.resume()

    def __calculateDownloadProgress(self):
        value = 0
        for progressBar in self.progressBarContainer:
            value += progressBar.value()

        percentage = self.__calculateDownloadPercentage(value, self._totalSize)  # 已下载百分比
        downloadedSize = self.__convertSizeToString(value)  # 转换已下载字节数为字符串表示
        elapsedTime = time.time() - self._lastTime  # 时间间隔
        downloadSpeed = self.__calculateDownloadSpeed(value, self._lastValue, elapsedTime)  # 下载速度
        remainingTime = self.__calculateRemainingTime(self._totalSize, value, downloadSpeed)  # 剩余时间

        self.stateItem.setText(f"{downloadedSize} ({percentage:.2f}%)")
        self.remainingTimeItem.setText(self.__convertSecondsToHms(remainingTime))
        self.downloadSpeedItem.setText(f"{self.__convertSizeToString(downloadSpeed)}/秒")

        self._lastValue, self._lastTime = value, time.time()
