from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QTableWidget, QPushButton
from PyQt6.uic import loadUi
from project.src.delegate.MenuDelegate import MenuDelegate
from project.src.model.MenuModel import MenuModel

class RestaurantMenuScreen(QWidget):
    IMAGE_SIZE = 80
    ROW_HEIGHT = 130

    def __init__(self, place_id, parent=None):
        super().__init__(parent)
        self.place_id = place_id
        self.parent = parent
        self.menu_model = MenuModel(place_id)
        print(f"RestaurantMenuScreen: Place ID used: {self.place_id}")
        self.setupUi()

    def setupUi(self):
        # Verify the UI file exists
        import os
        ui_file_path = "ui/menu_page.ui"  # Adjust this path if needed
        if not os.path.exists(ui_file_path):
            raise FileNotFoundError(f"UI file not found at: {ui_file_path}. Please check the path.")
        print(f"Loading UI file from: {ui_file_path}")

        # Load the UI
        try:
            loadUi(ui_file_path, self)
            print("UI file loaded successfully")
        except Exception as e:
            print(f"Error loading UI file: {e}")
            raise

        # Debug: Verify that all widgets are found
        self.filter_pushButton = self.findChild(QPushButton, "restaurant_info_button")  # Updated to match the UI
        if self.filter_pushButton is None:
            raise ValueError("restaurant_info_button (Filter) not found in the UI file. Check the objectName in menu_page.ui.")
        print("filter_pushButton found:", self.filter_pushButton)

        self.create_pushButton = self.findChild(QPushButton, "pushButton_3")  # "Add" button
        if self.create_pushButton is None:
            raise ValueError("pushButton_3 (Add) not found in the UI file. Check the objectName in menu_page.ui.")
        print("create_pushButton found:", self.create_pushButton)

        self.edit_pushButton = self.findChild(QPushButton, "pushButton_4")  # "Edit" button
        if self.edit_pushButton is None:
            raise ValueError("pushButton_4 (Edit) not found in the UI file. Check the objectName in menu_page.ui.")
        print("edit_pushButton found:", self.edit_pushButton)

        self.delete_pushButton = self.findChild(QPushButton, "pushButton_8")  # "Delete" button
        if self.delete_pushButton is None:
            raise ValueError("pushButton_8 (Delete) not found in the UI file. Check the objectName in menu_page.ui.")
        print("delete_pushButton found:", self.delete_pushButton)

        # Find the tableWidget placeholder
        table_widget_placeholder = self.findChild(QTableWidget, "tableWidget")
        if table_widget_placeholder is None:
            raise ValueError("tableWidget not found in the UI file. Check the objectName in menu_page.ui.")
        print("tableWidget placeholder found:", table_widget_placeholder)

        # Create a MenuDelegate instance
        self.tableWidget = MenuDelegate(self.place_id)
        self.tableWidget.setObjectName("tableWidget")
        print("MenuDelegate instance created:", self.tableWidget)

        # Replace the placeholder in the layout
        placeholder_layout = table_widget_placeholder.parent().layout()
        if placeholder_layout is None:
            raise ValueError("tableWidget placeholder is not in a layout. Check the UI file structure.")
        placeholder_index = placeholder_layout.indexOf(table_widget_placeholder)
        placeholder_layout.replaceWidget(table_widget_placeholder, self.tableWidget)
        print("tableWidget placeholder replaced with MenuDelegate")

        # Delete the placeholder to avoid memory leaks
        table_widget_placeholder.deleteLater()
        print("tableWidget placeholder deleted")

        # Set icons for the filter button
        filter_icon = QIcon(":/images/ic_adjust.png")
        if filter_icon.isNull():
            print("Warning: Filter icon not found at :/images/ic_adjust.png. Check your resource file.")
        self.filter_pushButton.setIcon(filter_icon)
        self.filter_pushButton.setIconSize(QtCore.QSize(15, 15))
        print("Filter button icon set")

        # Configure the tableWidget (now a MenuDelegate)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.tableWidget.itemClicked.connect(self.on_slotDelegate_byrow)
        print("tableWidget signals connected")

        # Load initial menu data
        self.load_menu_data()
        print("setupUi completed")

    def update_place_id(self, place_id):
        """Update place_id and reload menu data."""
        print(f"RestaurantMenuScreen: Updating place_id to {place_id}")
        self.place_id = place_id
        self.menu_model.set_place_id(place_id)  # Update place_id and reset offset
        self.tableWidget.place_id = place_id
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.load_menu_data()

    def load_menu_data(self):
        """Load menu data for the restaurant based on place_id."""
        try:
            if not self.place_id:
                print("load_menu_data: place_id is None, cannot load menu")
                self.tableWidget.clearContents()
                self.tableWidget.setRowCount(1)
                item = QtWidgets.QTableWidgetItem("No place_id provided. Please provide a valid place_id.")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(0, 0, item)
                return

            print(f"Loading menu for place_id: {self.place_id}")
            menu_items = self.menu_model.get_menu(use_pagination=True)

            print(f"Loaded menu items (initial load): {len(menu_items)} items")
            print(f"Menu items: {menu_items}")

            if not menu_items:
                print("No menu items to display.")
                print(f"MenuModel has_more: {self.menu_model.has_more()}")
                print(f"MenuModel offset: {self.menu_model.offset()}")
                self.tableWidget.clearContents()
                self.tableWidget.setRowCount(1)
                item = QtWidgets.QTableWidgetItem("No menu items available for this restaurant.")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(0, 0, item)
                return

            self.tableWidget.load_more_menu(menu_items)
            self.tableWidget.update()
            self.tableWidget.repaint()
            print(f"Total rows in table after initial load: {self.tableWidget.rowCount()}")
            print(f"Table widget visible: {self.tableWidget.isVisible()}")
        except AttributeError as e:
            print(f"Error in load_menu_data: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in load_menu_data: {e}")
            raise

    def on_scroll(self):
        """Load more menu items when scrolling to the bottom."""
        scroll_bar = self.tableWidget.verticalScrollBar()
        if scroll_bar.value() >= scroll_bar.maximum() - 10:
            print("Reached near end of scroll, loading more menu items...")
            if not self.place_id:
                print("on_scroll: place_id is None, cannot load more menu items")
                return

            menu_items = self.menu_model.get_menu(use_pagination=True)

            print(f"Loaded additional menu items: {len(menu_items)} items")
            print(f"Additional menu items: {menu_items}")

            if menu_items:
                self.tableWidget.load_more_menu(menu_items)
                print(f"Total rows in table after loading more: {self.tableWidget.rowCount()}")
            else:
                print("No more menu items to load.")

    def on_slotDelegate_byrow(self, item):
        """Handle row click events."""
        row = item.row()
        product_id = self.tableWidget.item(row, 0).text()
        item_name = self.tableWidget.item(row, 2).text()
        print(f"Selected menu item: product_id={product_id}, name={item_name}")

    def closeEvent(self, event):
        """Clean up resources when closing."""
        print("Closing RestaurantMenuScreen")
        self.menu_model.close_connection()
        if self.tableWidget:
            self.tableWidget.close()
        event.accept()
        print("RestaurantMenuScreen closed")