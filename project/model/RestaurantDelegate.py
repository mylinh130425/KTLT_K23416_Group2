from PyQt6.QtCore import QAbstractTableModel, Qt


class RestaurantDelegate(QAbstractTableModel):
    def __init__(self, restaurants=None):
        super().__init__()
        self.restaurants = restaurants or []

    def rowCount(self, parent=None):
        return len(self.restaurants)

    def columnCount(self, parent=None):
        return 7  # Number of columns in the table

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        restaurant = self.restaurants[index.row()]
        column = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                return restaurant.name
            elif column == 1:
                return f"{restaurant.rating} ⭐"
            elif column == 2:
                return restaurant.open_hours
            elif column == 3:
                return restaurant.category
            elif column == 4:
                return restaurant.address
            elif column == 5:
                return restaurant.hotline
            elif column ==6:
                return restaurant.accessibility

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        headers = ["Restaurant", "Rate", "Open - Close", "Category", "Address", "Hotline", "Accessibility"]
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return headers[section]
        return None
