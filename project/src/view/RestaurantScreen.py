from PyQt6.QtWidgets import QWidget, QVBoxLayout
from project.src.delegate.RestaurantDelegate import RestaurantDelegate

class RestaurantScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.restaurant_table = RestaurantDelegate()
        self.restaurant_table.verticalScrollBar().valueChanged.connect(self.on_scroll)

        layout.addWidget(self.restaurant_table)
        self.setLayout(layout)

    def on_scroll(self):
        """Tải thêm dữ liệu khi cuộn xuống cuối."""
        scrollbar = self.restaurant_table.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum():
            self.restaurant_table.load_more_restaurants()
