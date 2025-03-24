from PIL.ImageQt import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from project.src.delegate.MenuDelegate import MenuDelegate
from project.src.model.MenuModel import MenuModel


class RestaurantMenuScreen(QWidget):
    def __init__(self, place_id, parent=None):
        super().__init__(parent)
        self.parent = parent
        # Khởi tạo MenuModel
        self.menu_model = MenuModel(place_id)
        print(self.parent)
        # Thay thế tableWidget bằng MenuDelegate
        try:
            if not hasattr(self.parent, 'tableWidget'):
                raise AttributeError("tableWidget not found in UI.")
            #chỗ này parent chưa có tableWidget check lại
            self.parent.tableWidget.setParent(None)
            # self.parent.tableWidget=None
            self.parent.tableWidget = MenuDelegate(place_id)
            self.parent.tableWidget.setObjectName("tableWidget")
            self.parent.menu_verticalLayout.insertWidget(1, self.parent.tableWidget)
            # print("MenuDelegate added to verticalLayout_13.")
        except AttributeError as e:
            print(f"Error replacing tableWidget: {e}")
            return

        # Kích hoạt cuộn dọc
        self.parent.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.parent.tableWidget.verticalScrollBar().valueChanged.connect(self.on_scroll)

        # Kết nối sự kiện khi người dùng chọn một hàng
        self.parent.tableWidget.itemClicked.connect(self.on_slotDelegate_byrow)

        # Load dữ liệu menu ban đầu
        self.load_menu_data()
        """
        TODO: Check laị hết các component đã add vào ui và đổi self của nó thành self.parent
        """
        #Đặt tiêu đề và hình ảnh
        self.parent.restaurant_name_label.setText("All Restaurants Menu" if place_id is None else "Restaurant Menu")
        pixmap = QPixmap("restaurant_image.jpg")
        if not pixmap.isNull():
            self.parent.restaurant_photo_label.setPixmap(pixmap)
            self.parent.restaurant_photo_label.setScaledContents(True)
        else:
            self.parent.restaurant_photo_label.setText("No Image")

        # Kết nối các nút
        self.parent.restaurant_info_button.clicked.connect(self.show_info)
        self.parent.restaurant_menu_button.clicked.connect(self.show_menu)
        self.parent.restaurant_review_button.clicked.connect(self.show_review)

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

        self.parent.tableWidget.load_more_menu(menu_items)

        # Kiểm tra tổng số hàng sau khi tải
        print(f"Total rows in table after initial load: {self.parent.tableWidget.rowCount()}")

    def on_scroll(self):
        """Tự động load thêm dữ liệu khi người dùng cuộn đến cuối danh sách."""
        scroll_bar = self.parent.tableWidget.verticalScrollBar()
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
                self.parent.tableWidget.load_more_menu(menu_items)
                print(f"Total rows in table after loading more: {self.parent.tableWidget.rowCount()}")
            else:
                print("No more menu items to load.")

    def on_slotDelegate_byrow(self, item):
        """Xử lý khi người dùng chọn một hàng trong MenuDelegate."""
        row = item.row()
        product_id = self.parent.tableWidget.item(row, 0).text()
        item_name = self.parent.tableWidget.item(row, 2).text()
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
