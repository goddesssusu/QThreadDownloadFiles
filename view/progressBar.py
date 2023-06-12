
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QProgressBar

from threads.subDownloadFile import SubDownloadFile


class ProgressBar(QProgressBar):

    def __init__(self, index, url, startByte, endByte, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setRange(0, endByte-startByte+1)
        self._subDownloadFile = SubDownloadFile(
            index=index, url=url, startByte=startByte, endByte=endByte, parent=self)
        self._subDownloadFile.downloadProgress.connect(self.setValue)
        self._subDownloadFile.downloadFinished.connect(lambda: print(self.value()))
        self._subDownloadFile.start()

    def resume(self):
        self._subDownloadFile.resume()

    def pause(self):
        self._subDownloadFile.pause()
