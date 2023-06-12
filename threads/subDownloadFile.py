import os

from PyQt6.QtCore import QThread, pyqtSignal, QUrl, QCoreApplication
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class SubDownloadFile(QThread):
    """
    文件下载子线程
    """
    downloadFinished = pyqtSignal()
    downloadProgress = pyqtSignal(int)

    def __init__(self, index, url, startByte, endByte, *args, **kwargs):
        super(SubDownloadFile, self).__init__(*args, **kwargs)
        self._url = url
        self._startByte = startByte
        self._endByte = endByte
        self._networkManager = QNetworkAccessManager(parent=self)
        self._reply = None
        self._downloadedBytes = 0  # 记录已下载的字节数
        self._fileName = self._url.split('/')[-1]  # 获取文件名
        self._tempFileName = f"{self._fileName}[{index}].temp"  # 临时文件名
        if os.path.exists(self._tempFileName):
            self._downloadedBytes = os.path.getsize(self._tempFileName)

    def run(self) -> None:
        request = QNetworkRequest(QUrl(self._url))
        # 设置 "Range" 请求头，从已下载的字节数开始下载
        request.setRawHeader(
            b"Range", f"""bytes={min(self._endByte, max(
                self._downloadedBytes, self._startByte))}-{self._endByte}""".encode())

        self._reply = self._networkManager.get(request)
        self._reply.downloadProgress.connect(self.__emitDownloadProgress)
        self._reply.readyRead.connect(self._readyRead)
        self._reply.finished.connect(self.__downloadFinished)

        while self._reply is not None:
            if self._reply.isFinished():
                break

            self.msleep(10)
            QCoreApplication.processEvents()  # 显式处理事件循环

    def __emitDownloadProgress(self, bytes_received, bytes_total):
        self.downloadProgress.emit(bytes_received)

    def _readyRead(self):
        if self._reply is not None:
            self._downloadedBytes += self._reply.bytesAvailable()  # 获取当前已下载的字节数
            # self.downloadProgress.emit(self._downloadedBytes)
            content = self._reply.readAll()
            with open(self._tempFileName, 'ab') as file:
                file.write(content)

    def __downloadFinished(self):
        if self._reply.error() == QNetworkReply.NetworkError.NoError:
            self._downloadedBytes += self._reply.bytesAvailable()
            # self.downloadProgress.emit(self._downloadedBytes)
            content = self._reply.readAll()
            self._reply.deleteLater()
            self._reply = None
            # 合并临时文件到最终临时文件
            with open(self._tempFileName, 'ab') as file:
                file.write(content)
            self.downloadFinished.emit()
            print(self._downloadedBytes, self._startByte, self._endByte)

            # os.remove(self._tempFileName)  # 删除临时文件

    def pause(self):
        if self._reply is not None and self._reply.isRunning():
            self._reply.abort()  # 中止当前下载请求

    def resume(self):
        if self._reply is not None and not self._reply.isRunning():
            self.run()
