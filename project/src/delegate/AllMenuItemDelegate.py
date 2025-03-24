from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from project.src.model.MenuModel import MenuModel

class AllMenuItemDelegate(QTableWidget):
    def __init__(self):
        super().__init__()
        self.model = MenuModel(place_id=None)  # place_id=None vì lấy tất cả menu
        table_headers = ["_id", "Restaurant", "Item", "Rate", "Price", "Description", "Review"]
        self.setColumnCount(len(table_headers))
        self.setHorizontalHeaderLabels(table_headers)

        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

    def load_more_menu(self, menu_items):
        print(f"AllMenuItemDelegate: Loading {len(menu_items)} menu items")
        try:
            for menu_item in menu_items:
                row = self.rowCount()
                self.insertRow(row)

                # Đảm bảo các trường tồn tại và có giá trị hợp lệ
                self.setItem(row, 0, QTableWidgetItem(str(menu_item.get("_id", "N/A"))))
                self.setItem(row, 1, QTableWidgetItem(str(menu_item.get("restaurant_name", "N/A"))))
                self.setItem(row, 2, QTableWidgetItem(str(menu_item.get("Item", "N/A"))))
                self.setItem(row, 3, QTableWidgetItem(str(menu_item.get("Rate", 0.0))))
                self.setItem(row, 4, QTableWidgetItem(str(menu_item.get("Price", 0))))
                self.setItem(row, 5, QTableWidgetItem(str(menu_item.get("Description", "N/A"))))
                # Xử lý Review (có thể là danh sách)
                reviews = menu_item.get("Review", [])
                review_text = "\n".join([str(review) for review in reviews]) if reviews else "No reviews"
                self.setItem(row, 6, QTableWidgetItem(review_text))

                self.setRowHeight(row, 50)
        except Exception as e:
            print(f"Error in AllMenuItemDelegate.load_more_menu: {e}")