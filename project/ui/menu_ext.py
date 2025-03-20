import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from menu import Ui_MainWindow
from menu_delegate import MenuDelegate
from project.ui.MenuModel import MenuModel


class MealMatchUI(QMainWindow, Ui_MainWindow):
    def __init__(self, place_id=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("MealMatch - List Menu")

        # Khởi tạo MenuModel
        self.menu_model = MenuModel(place_id)

        # Thay thế tableWidget bằng MenuDelegate
        try:
            if not hasattr(self, 'tableWidget'):
                raise AttributeError("tableWidget not found in UI.")
            self.tableWidget.setParent(None)
            self.tableWidget = MenuDelegate()
            self.tableWidget.setObjectName("tableWidget")
            self.verticalLayout_13.insertWidget(1, self.tableWidget)
            print("MenuDelegate added to verticalLayout_13.")
        except AttributeError as e:
            print(f"Error replacing tableWidget: {e}")
            return

        # Kích hoạt cuộn dọc
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.on_scroll)

        # Kết nối sự kiện khi người dùng chọn một hàng
        self.tableWidget.itemClicked.connect(self.on_slotDelegate_tu_row)

        # Load dữ liệu menu ban đầu
        self.load_menu_data()

        # Đặt tiêu đề và hình ảnh
        self.restaurant_name_label.setText("All Restaurants Menu" if place_id is None else "Restaurant Menu")
        pixmap = QPixmap("restaurant_image.jpg")
        if not pixmap.isNull():
            self.restaurant_photo_label.setPixmap(pixmap)
            self.restaurant_photo_label.setScaledContents(True)
        else:
            self.restaurant_photo_label.setText("No Image")

        # Kết nối các nút
        self.restaurant_info_button.clicked.connect(self.show_info)
        self.restaurant_menu_button.clicked.connect(self.show_menu)
        self.restaurant_review_button.clicked.connect(self.show_review)

    def load_menu_data(self):
        """Lấy dữ liệu từ MenuModel và hiển thị lên bảng."""
        if self.menu_model.place_id:
            menu_items = self.menu_model.get_menu(use_pagination=True)
        else:
            menu_items = self.menu_model.get_all_menus(use_pagination=True)

        print(f"Loaded menu items (initial load): {len(menu_items)} items")
        print(f"Menu items: {menu_items}")

        if not menu_items:
            print("No menu items to display.")
            return

        self.tableWidget.load_more_menu(menu_items)

        # Kiểm tra tổng số hàng sau khi tải
        print(f"Total rows in table after initial load: {self.tableWidget.rowCount()}")

    def on_scroll(self):
        """Tự động load thêm dữ liệu khi người dùng cuộn đến cuối danh sách."""
        scroll_bar = self.tableWidget.verticalScrollBar()
        # Kiểm tra nếu cuộn gần đến cuối (thay vì chỉ khi đạt maximum)
        if scroll_bar.value() >= scroll_bar.maximum() - 10:  # Giảm ngưỡng để tải sớm hơn
            print("Reached near end of scroll, loading more menu items...")
            if self.menu_model.place_id:
                menu_items = self.menu_model.get_menu(use_pagination=True)
            else:
                menu_items = self.menu_model.get_all_menus(use_pagination=True)

            print(f"Loaded additional menu items: {len(menu_items)} items")
            print(f"Additional menu items: {menu_items}")

            if menu_items:
                self.tableWidget.load_more_menu(menu_items)
                print(f"Total rows in table after loading more: {self.tableWidget.rowCount()}")
            else:
                print("No more menu items to load.")

    def on_slotDelegate_tu_row(self, item):
        """Xử lý khi người dùng chọn một hàng trong MenuDelegate."""
        row = item.row()
        product_id = self.tableWidget.item(row, 0).text()
        item_name = self.tableWidget.item(row, 2).text()
        print(f"Selected menu item: product_id={product_id}, name={item_name}")

    def show_info(self):
        print("Show Info")

    def show_menu(self):
        print("Show Menu")

    def show_review(self):
        print("Show Review")

    def closeEvent(self, event):
        self.menu_model.close_connection()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MealMatchUI()  # Không truyền place_id để hiển thị List Menu
    window.show()
    sys.exit(app.exec())