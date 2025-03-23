import requests
from io import BytesIO

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class ImageLoader(QThread):
    """Thread for asynchronous image loading."""
    image_loaded = pyqtSignal(int, QPixmap)  # Signal emitted when image is loaded

    def __init__(self, row, url):
        super().__init__()
        self.row = row
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url)
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(response.content).getvalue())
            if not pixmap.isNull():
                pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
                self.image_loaded.emit(self.row, pixmap)
        except Exception as e:
            print(f"Error loading image for row {self.row}: {e}")
