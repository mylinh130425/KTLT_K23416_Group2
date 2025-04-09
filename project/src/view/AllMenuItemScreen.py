from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QComboBox, \
    QLabel
from project.src.delegate.MenuDelegate import MenuDelegate
from project.src.filter_menu import query_dishes
from project.src.model.MenuModel import MenuModel


class FilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filter Menu Items")
        self.setModal(True)
        self.setupUi()

    def setupUi(self):
        layout = QFormLayout(self)

        self.category_input = QLineEdit(self)
        self.min_price_input = QLineEdit(self)
        self.max_price_input = QLineEdit(self)
        self.min_rating_input = QLineEdit(self)
        self.sort_order_input = QComboBox(self)
        self.sort_order_input.addItems(["Low to High (1)", "High to Low (-1)"])

        layout.addRow(QLabel("Category (food, drink, ...):"), self.category_input)
        layout.addRow(QLabel("Min Price (VND):"), self.min_price_input)
        layout.addRow(QLabel("Max Price (VND):"), self.max_price_input)
        layout.addRow(QLabel("Min Rating (1-5):"), self.min_rating_input)
        layout.addRow(QLabel("Sort by Price:"), self.sort_order_input)

        self.apply_button = QPushButton("Apply Filter", self)
        self.apply_button.clicked.connect(self.accept)
        layout.addWidget(self.apply_button)

    def get_filter_values(self):
        category = self.category_input.text().strip() or None
        try:
            min_price = float(self.min_price_input.text().strip() or 0)
        except ValueError:
            min_price = 0
        try:
            max_price = float(self.max_price_input.text().strip() or 1_000_000)
        except ValueError:
            max_price = 1_000_000
        try:
            min_rating = float(self.min_rating_input.text().strip() or 0)
        except ValueError:
            min_rating = 0
        sort_order = 1 if self.sort_order_input.currentIndex() == 0 else -1
        return category, min_price, max_price, min_rating, sort_order


class AllMenuItemScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.menu_model = MenuModel()
        print("AllMenuItemScreen: Initialized")
        self.current_filter = {
            "category": None,
            "min_price": 0,
            "max_price": 1_000_000,
            "min_rating": 0,
            "sort_order": 1
        }
        self.current_page = 0
        self.items_per_page = 10
        self.is_filtered = False
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)
        button_layout.setSpacing(10)

        self.filter_pushButton = QPushButton()
        self.filter_pushButton.setText("Filter")
        filter_icon = QIcon(":/images/ic_adjust.png")
        self.filter_pushButton.setIcon(filter_icon)
        self.filter_pushButton.setIconSize(QtCore.QSize(15, 15))
        self.filter_pushButton.setObjectName("filter_pushButton")
        button_layout.addWidget(self.filter_pushButton)
        self.filter_pushButton.clicked.connect(self.show_filter_dialog)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.tableWidget = MenuDelegate()
        self.tableWidget.setObjectName("tableWidget")
        layout.addWidget(self.tableWidget)

        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.on_scroll)

        self.load_menu_data()

    def show_filter_dialog(self):
        dialog = FilterDialog(self)
        if dialog.exec():
            category, min_price, max_price, min_rating, sort_order = dialog.get_filter_values()
            self.apply_filter(category, min_price, max_price, min_rating, sort_order)

    def apply_filter(self, category, min_price, max_price, min_rating, sort_order):
        print(
            f"AllMenuItemScreen: Applying filter - Category: {category}, Min Price: {min_price}, Max Price: {max_price}, Min Rating: {min_rating}, Sort Order: {sort_order}")

        self.current_filter = {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "min_rating": min_rating,
            "sort_order": sort_order
        }
        self.current_page = 0
        self.is_filtered = True

        filtered_items = self.get_paginated_items()
        print(f"AllMenuItemScreen: Raw filtered items: {filtered_items}")
        standardized_items = self.standardize_items(filtered_items)

        print(f"AllMenuItemScreen: Filtered items: {len(standardized_items)} items")
        print(f"AllMenuItemScreen: Standardized filtered data: {standardized_items}")

        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        if not standardized_items:
            self.tableWidget.setRowCount(1)
            item = QtWidgets.QTableWidgetItem("No items match the filter.")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.setItem(0, 0, item)
        else:
            self.tableWidget.load_more_menu(standardized_items)

        self.tableWidget.update()
        self.tableWidget.repaint()
        print(f"AllMenuItemScreen: Total rows in table after filtering: {self.tableWidget.rowCount()}")

    def standardize_items(self, items):
        standardized_items = []
        for item in items:
            # Tính average_rating từ food_review
            food_reviews = item.get("food_review", [])
            average_rating = 0
            if food_reviews:
                total_rating = 0
                count = 0
                for review in food_reviews:
                    taste = review.get("rating", {}).get("taste", 0)
                    portion = review.get("rating", {}).get("portion", 0)
                    hygiene = review.get("rating", {}).get("hygiene", 0)
                    if taste or portion or hygiene:
                        total_rating += (taste + portion + hygiene) / 3
                        count += 1
                average_rating = total_rating / count if count > 0 else 0

            # Ưu tiên sử dụng rating từ MongoDB nếu có (cho query_dishes)
            rating_from_db = item.get("rating", 0)
            final_rating = rating_from_db if rating_from_db > 0 else (item.get("average_rating", average_rating if average_rating > 0 else item.get("Rate", 0)))

            # Xử lý trường ảnh: query_dishes() dùng feature_img, menu_model.get_all_menus() dùng featured_image
            image_url = item.get("feature_img", item.get("featured_image", ""))

            # Kiểm tra và log các trường quan trọng
            print(f"AllMenuItemScreen: Item - {item.get('dish_name', item.get('Item', 'N/A'))}:")
            print(f"  feature_img: {item.get('feature_img', 'Not found')}")
            print(f"  featured_image: {item.get('featured_image', 'Not found')}")
            print(f"  selected image_url: {image_url}")
            print(f"  food_review: {food_reviews}")
            print(f"  average_rating (calculated): {average_rating}")
            print(f"  rating (from MongoDB): {rating_from_db}")
            print(f"  final_rating: {final_rating}")

            standardized_item = {
                "_id": item.get("place_id", item.get("_id", "N/A")),
                "featured_image": image_url,  # Sử dụng image_url đã chọn
                "Item": item.get("dish_name", item.get("Item", "N/A")),
                "Rate": final_rating,
                "Price": item.get("price", item.get("Price", 0)),
                "restaurant_name": item.get("restaurant_name", "N/A"),
                "category": item.get("category", "N/A"),
                "Description": item.get("description", item.get("Description", "N/A")),
                "Review": [str(review) for review in item.get("review_text", item.get("Review", []))]
            }
            standardized_items.append(standardized_item)
        return standardized_items

    def get_paginated_items(self):
        if not self.is_filtered:
            return self.menu_model.get_all_menus(use_pagination=True)

        skip = self.current_page * self.items_per_page
        filtered_items = query_dishes(
            category=self.current_filter["category"],
            min_price=self.current_filter["min_price"],
            max_price=self.current_filter["max_price"],
            min_rating=self.current_filter["min_rating"],
            sort_order=self.current_filter["sort_order"],
            skip=skip,
            limit=self.items_per_page
        )
        return filtered_items

    def load_menu_data(self):
        try:
            print("AllMenuItemScreen: Loading all menu items")
            menu_items = self.menu_model.get_all_menus(use_pagination=True)

            print(f"AllMenuItemScreen: Loaded menu items (initial load): {len(menu_items)} items")
            print(f"AllMenuItemScreen: Raw menu items: {menu_items}")

            if not menu_items:
                print("AllMenuItemScreen: No menu items to display.")
                self.tableWidget.clearContents()
                self.tableWidget.setRowCount(1)
                item = QtWidgets.QTableWidgetItem("No menu items available.")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(0, 0, item)
                return

            standardized_items = self.standardize_items(menu_items)
            print(f"AllMenuItemScreen: Standardized menu items: {standardized_items}")
            self.tableWidget.load_more_menu(standardized_items)
            self.tableWidget.update()
            self.tableWidget.repaint()
            print(f"AllMenuItemScreen: Total rows in table after initial load: {self.tableWidget.rowCount()}")
        except AttributeError as e:
            print(f"AllMenuItemScreen: Error in load_menu_data: {e}")

    def on_scroll(self):
        scroll_bar = self.tableWidget.verticalScrollBar()
        if scroll_bar.value() >= scroll_bar.maximum() - 10:
            print("AllMenuItemScreen: Reached near end of scroll, loading more menu items...")
            if self.is_filtered:
                self.current_page += 1
            menu_items = self.get_paginated_items()

            print(f"AllMenuItemScreen: Loaded additional menu items: {len(menu_items)} items")
            print(f"AllMenuItemScreen: Raw additional menu items: {menu_items}")

            if menu_items:
                standardized_items = self.standardize_items(menu_items)
                print(f"AllMenuItemScreen: Standardized additional menu items: {standardized_items}")
                self.tableWidget.load_more_menu(standardized_items)
                print(f"AllMenuItemScreen: Total rows in table after loading more: {self.tableWidget.rowCount()}")
            else:
                print("AllMenuItemScreen: No more menu items to load.")
                if self.is_filtered:
                    self.current_page -= 1

    def closeEvent(self, event):
        self.menu_model.close_connection()
        self.tableWidget.close()
        event.accept()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = AllMenuItemScreen()
    window.show()
    sys.exit(app.exec())