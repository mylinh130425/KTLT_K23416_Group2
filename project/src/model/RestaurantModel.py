from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout
from project.src.delegate.RestaurantDelegate import RestaurantDelegate
from project.src.DatabaseManager import DatabaseManager


class RestaurantModel(QtWidgets.QWidget):  # Kế thừa từ QWidget
    def __init__(self, parent=None):
        """
        Initialize the RestaurantModel widget, set up the layout, database manager,
        and load the initial batch of restaurants into the table. Connect the
        scrollbar to detect scrolling and load more data as needed.

        Parameters:
        parent (QWidget, optional): The parent widget of this RestaurantModel. Defaults to None.
        """
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.db_manager = DatabaseManager()
        self.offset = 0  # Track loaded data position
        self.limit = 15   # Load 15 restaurants per batch

        restaurants = self.db_manager.get_restaurants(self.offset, self.limit)

        # Create Model and View
        self.restaurant_table = RestaurantDelegate(restaurants, offset=self.offset)
        # Enable scrolling detection
        self.restaurant_table.verticalScrollBar().valueChanged.connect(self.on_scroll)

        layout.addWidget(self.restaurant_table)
        self.setLayout(layout)

        col_count = self.restaurant_table.columnCount()
        self.restaurant_table.hideColumn(0)
        for i in range(col_count):
            self.restaurant_table.setColumnWidth(i, 150)

        layout.addWidget(self.restaurant_table)
        self.setLayout(layout)
        super().__init__(parent)
        layout = QVBoxLayout(self)


        self.db_manager = DatabaseManager()
        self.offset = 0  # Track loaded data position
        self.limit = 15   # Load 15 restaurants per batch


        restaurants = self.db_manager.get_restaurants(self.offset, self.limit)

        # Create Model and View
        self.restaurant_table = RestaurantDelegate(restaurants,offset=self.offset)
        # Enable scrolling detection
        self.restaurant_table.verticalScrollBar().valueChanged.connect(self.on_scroll)

        # Load initial batch
        # self.restaurant_table.

        layout.addWidget(self.restaurant_table)
        self.setLayout(layout)

        col_count = self.restaurant_table.columnCount()
        self.restaurant_table.hideColumn(0)
        for i in range(col_count):
            self.restaurant_table.setColumnWidth(i,150)

        layout.addWidget(self.restaurant_table)
        self.setLayout(layout)

    def on_scroll(self):
        """Detect when user scrolls to the bottom and load more data."""
        scrollbar = self.restaurant_table.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum():  # User reached bottom
            self.restaurant_table.load_more_restaurants()