
from PyQt6.QtCore import QThread, pyqtSignal, QUrl, QCoreApplication
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class GetTotalSize(QThread):
    """
    获取文件总大小
    """
    totalSize = pyqtSignal(int, str)

    def __init__(self, *args, **kwargs):
        super(GetTotalSize, self).__init__(*args, **kwargs)
        self.network_manager = QNetworkAccessManager(parent=self)
        self.url = ''
        self.totalSize.connect(print)

    def run(self) -> None:
        request = QNetworkRequest(QUrl(self.url))
        request.setRawHeader(b"Request-Method", b"HEAD")
        self.reply = self.network_manager.head(request)
        self.reply.finished.connect(self.__finished)

        while not self.reply.isFinished():
            self.msleep(10)
            QCoreApplication.processEvents()

    def __finished(self):
        if self.reply.error() == QNetworkReply.NetworkError.NoError:
            # 获取文件的总大小
            total_size = self.reply.header(
                QNetworkRequest.KnownHeaders.ContentLengthHeader)
            self.totalSize.emit(total_size, self.url)
        self.reply.deleteLater()