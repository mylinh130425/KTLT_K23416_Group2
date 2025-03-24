import requests
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap

class ImageLoaderSignals(QObject):
    """Class để chứa các signal, vì QRunnable không hỗ trợ signal trực tiếp."""
    image_loaded = pyqtSignal(int, QPixmap)

class ImageLoader(QRunnable):
    def __init__(self, row, url):
        super().__init__()
        self.row = row
        self.url = url
        self.signals = ImageLoaderSignals()

    def run(self):
        try:
            # print(f"ImageLoader: Loading image from {self.url} for row {self.row}")
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            # print(f"ImageLoader: Image loaded successfully for row {self.row}")
            self.signals.image_loaded.emit(self.row, pixmap)
        except Exception as e:
            # print(f"ImageLoader: Failed to load image from {self.url}: {e}")
            self.signals.image_loaded.emit(self.row, QPixmap())