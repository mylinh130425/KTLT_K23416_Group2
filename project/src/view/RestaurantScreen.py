from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6 import QtWidgets
from project.src.delegate.RestaurantDelegate import RestaurantDelegate
from project.src.view.MenuScreen import MenuScreen


class RestaurantScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.parent = parent

        self.restaurant_table = RestaurantDelegate()
        self.restaurant_table.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.restaurant_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Disable editing
        self.restaurant_table.cellDoubleClicked.connect(self.open_menu_screen)

        layout.addWidget(self.restaurant_table)
        self.setLayout(layout)

    def on_scroll(self):
        """Tải thêm dữ liệu khi cuộn xuống cuối."""
        scrollbar = self.restaurant_table.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum():
            self.restaurant_table.load_more_restaurants()
    def open_menu_screen(self, row):
        """Mở trang menu khi double-click vào nhà hàng."""
        place_id = self.restaurant_table.item(row, 0).text()  # Lấy ID nhà hàng
        print(place_id)
        print(self.parent)
        self.parent.menu_page = MenuScreen(place_id, self.parent)
        # self.parent.setCurrentWidget(self.parent.menu_page) TODO: chuyển đúng trang inside_restaurant_page
        #rồi set cái stacked widget bên trong vào đúng trang menu_page

