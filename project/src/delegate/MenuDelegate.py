from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from project.src.model.MenuModel import MenuModel

class MenuDelegate(QTableWidget):
    def __init__(self, place_id):
        super().__init__()
        self.model = MenuModel(place_id)
        tabel_headers = ["_id"," ","Food", "Rate", "Price", "Description", "Review"]
        self.setColumnCount(len(tabel_headers))

        self.setHorizontalHeaderLabels(tabel_headers)
        self.load_more_menu()

    def load_more_menu(self):
        """Nạp dữ liệu từ model vào bảng."""
        menu_items = self.model.get_menu()
        if not menu_items:
            return
        current_row_count = self.rowCount()
        self.setRowCount(current_row_count + len(menu_items))

        """
        TODO:Chi - tìm cách để QTableWidgetItem hiển thị được các Widget hình ảnh, label thay
        vì chỉ có text
        """
        for i, item in enumerate(menu_items):
            row = current_row_count + i
            self.setItem(row, 0, QTableWidgetItem(item["_id"]))
            self.setItem(row, 1, QTableWidgetItem(item["featured_image"]))
            self.setItem(row, 2, QTableWidgetItem(item["name"]))
            self.setItem(row, 3, QTableWidgetItem(f"{item['rating']} ⭐"))
            self.setItem(row, 4, QTableWidgetItem(f"{item['price']} đ"))
            self.setItem(row, 5, QTableWidgetItem(item["description"]))
            self.setItem(row, 6, QTableWidgetItem(item["review"]))
        self.setColumnHidden(0,True)
        self.model.offset += len(menu_items)