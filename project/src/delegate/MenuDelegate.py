from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from project.src.model.MenuModel import MenuModel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests
from io import BytesIO

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class ImageLoader(QThread): #Thêm vào để đỡ lag khi Scroll xuống
    """Luồng để tải hình ảnh bất đồng bộ."""
    image_loaded = pyqtSignal(int, QPixmap)  # Tín hiệu gửi về khi hình ảnh tải xong

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


class MenuDelegate(QTableWidget):
    def __init__(self, place_id):
        super().__init__()
        self.model = MenuModel(place_id)
        tabel_headers = ["_id"," ","Food", "Rate", "Price", "Description", "Review"]
        self.setColumnCount(len(tabel_headers))

        self.setHorizontalHeaderLabels(tabel_headers)
        self.load_more_menu()

    #
    # def load_more_menu(self):
    #     """Nạp dữ liệu từ model vào bảng."""
    #     menu_items = self.model.get_menu()
    #     if not menu_items:
    #         return
    #     current_row_count = self.rowCount()
    #     self.setRowCount(current_row_count + len(menu_items))
    #
    #     """
    #     TODO:Chi - tìm cách để QTableWidgetItem hiển thị được các Widget hình ảnh, label thay
    #     vì chỉ có text
    #     """
    #     for i, item in enumerate(menu_items):
    #         row = current_row_count + i
    #         self.setItem(row, 0, QTableWidgetItem(item["_id"]))
    #         self.setItem(row, 1, QTableWidgetItem(item["featured_image"]))
    #         self.setItem(row, 2, QTableWidgetItem(item["name"]))
    #         self.setItem(row, 3, QTableWidgetItem(f"{item['rating']} ⭐"))
    #         self.setItem(row, 4, QTableWidgetItem(f"{item['price']} đ"))
    #         self.setItem(row, 5, QTableWidgetItem(item["description"]))
    #         self.setItem(row, 6, QTableWidgetItem(item["review"]))
    #     self.setColumnHidden(0,True)
    #     self.model.offset += len(menu_items)

