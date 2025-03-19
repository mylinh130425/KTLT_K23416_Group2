from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QTableView
from project.model.RestaurantDelegate import RestaurantDelegate
from project.model.data.Restaurant import Restaurant


class RestaurantScreen(QtWidgets.QWidget):  # Kế thừa từ QWidget
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Sample Data
        restaurants = [
            Restaurant("JAPAN DO", 5.0, "Mon - Fri: 8:00 - 21:00\nSat: 8:00 - 23:00\nSun: Off",
                       "Restaurant", "189 D. Cống Quỳnh, Quận 1, HCM", "0123456789", "Delivery"),
            Restaurant("JAPAN DO", 5.0, "Mon - Fri: 8:00 - 21:00\nSat: 8:00 - 23:00\nSun: Off",
                       "Restaurant", "189 D. Cống Quỳnh, Quận 1, HCM", "0123456789", "Takeout"),
        ]

        # Create Model and View
        self.model = RestaurantDelegate(restaurants)
        self.view = QTableView()
        self.view.setModel(self.model)

        # Adjust Column Widths
        self.view.setColumnWidth(0, 150)
        self.view.setColumnWidth(1, 80)
        self.view.setColumnWidth(2, 200)
        self.view.setColumnWidth(3, 100)
        self.view.setColumnWidth(4, 250)
        self.view.setColumnWidth(5, 120)

        layout.addWidget(self.view)
        self.setLayout(layout)
