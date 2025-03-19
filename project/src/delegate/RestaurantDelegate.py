from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from project.src.model.RestaurantModel import RestaurantModel

class RestaurantDelegate(QTableWidget):
    def __init__(self):
        super().__init__()
        self.model = RestaurantModel()  # Gọi model để lấy dữ liệu
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels([
            "_id", "", "Restaurant", "Rate", "Open - Close", "Category", "Address", "Hotline", "Accessibility"
        ])
        self.load_more_restaurants()

    def load_more_restaurants(self):
        """Nạp thêm dữ liệu vào bảng."""
        restaurants = self.model.get_restaurants()
        if not restaurants:
            return

        current_row_count = self.rowCount()
        self.setRowCount(current_row_count + len(restaurants))
        """
        TODO:Bản - tìm cách để QTableWidgetItem hiển thị được các Widget hình ảnh, label thay
        vì chỉ có text
        """
        for i, restaurant in enumerate(restaurants):
            row = current_row_count + i
            self.setItem(row, 0, QTableWidgetItem(str(restaurant["_id"])))  # Cột ẩn
            self.setItem(row,1, QTableWidgetItem(str(restaurant["featured_image"]))) #đang hiển thị link chưa hiển thị hình ảnh
            self.setItem(row, 2, QTableWidgetItem(restaurant["name"]))
            self.setItem(row, 3, QTableWidgetItem(f"{restaurant['rating']} ⭐"))
            self.setItem(row, 4, QTableWidgetItem(restaurant["open_hours"]))
            self.setItem(row, 5, QTableWidgetItem(restaurant["category"]))
            self.setItem(row, 6, QTableWidgetItem(restaurant["address"]))
            self.setItem(row, 7, QTableWidgetItem(restaurant["hotline"]))
            self.setItem(row, 8, QTableWidgetItem(str(restaurant["accessibility"])))

        self.model.offset += len(restaurants)  # Cập nhật offset
