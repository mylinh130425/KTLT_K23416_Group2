from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

class RestaurantDelegate(QTableWidget):
    def __init__(self, restaurants=None, offset=0):
        """
        Initialize a RestaurantDelegate object.

        Parameters
        ----------
        restaurants : list, optional
            List of Restaurant objects. If not provided, an empty list is used.
        offset : int, optional
            Starting index for loading restaurants. Defaults to 0.

        Notes
        -----
        After initialization, the load_more_restaurants() method is called to load
        an initial batch of restaurants.
        """
        super().__init__()
        self.offset = offset
        self.restaurants = restaurants or []
        self.setColumnCount(8)  # Số cột
        self.setHorizontalHeaderLabels(["_id","Restaurant", "Rate", "Open - Close", "Category", "Address", "Hotline", "Accessibility"])
        # Load initial batch
        self.load_more_restaurants()

    def load_more_restaurants(self):
        """Load next batch of restaurants from MongoDB."""

        if not self.restaurants:
            return  # No more data

        current_row_count = self.rowCount()
        self.setRowCount(current_row_count + len(self.restaurants))

        for i, restaurant in enumerate(self.restaurants):
            row = current_row_count + i
            """
            TODO: Bản - Sửa QTableWidgetItem để nó có thể hiển thị được các Widget khác ngoài text
            """
            self.setItem(row, 0, QTableWidgetItem(str(restaurant["_id"])))  # Cột ẩn
            self.setItem(row, 1, QTableWidgetItem(restaurant["name"]))
            self.setItem(row, 2, QTableWidgetItem(f"{restaurant['rating']} ⭐"))
            self.setItem(row, 3, QTableWidgetItem(restaurant["open_hours"]))
            self.setItem(row, 4, QTableWidgetItem(restaurant["category"]))
            self.setItem(row, 5, QTableWidgetItem(restaurant["address"]))
            self.setItem(row, 6, QTableWidgetItem(restaurant["hotline"]))
            self.setItem(row, 7, QTableWidgetItem(str(restaurant["accessibility"])))

        self.offset += len(self.restaurants)  # Update offset


