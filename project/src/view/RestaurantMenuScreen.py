import requests
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QByteArray, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QPainterPath
from PyQt6.QtWidgets import QWidget, QTableWidget
from PyQt6.uic import loadUi
from project.src.delegate.MenuDelegate import MenuDelegate
from project.src.model.MenuModel import MenuModel
from project.src.DatabaseManager import DatabaseManager

class RestaurantMenuScreen(QWidget):
    def __init__(self, place_id, parent=None):
        super().__init__(parent)
        self.place_id = place_id
        self.parent = parent
        self.menu_model = MenuModel(place_id)
        self.db_manager = DatabaseManager()
        print(f"RestaurantMenuScreen: Place ID used: {self.place_id}")
        self.setupUi()

        # get restaurant data for name and featured image
        self.restaurant_data = self.parent.db_manager.get_restaurant_byid(place_id)
        print(self.restaurant_data)
        print(f"RestaurantMenuScreen: Place ID used: {self.place_id}")
        if self.place_id is None:
            self.setupUi()
        else:
            self.updateUi()

    def updateUi(self):
        # Debug: Check if the parent and restaurant_photo_label exist
        print(f"Parent exists: {self.parent is not None}")
        print(f"Restaurant photo label exists: {hasattr(self.parent, 'restaurant_photo_label')}")
        if hasattr(self.parent, 'restaurant_photo_label'):
            print(f"Restaurant photo label visible: {self.parent.restaurant_photo_label.isVisible()}")
            print(f"Restaurant photo label size before: {self.parent.restaurant_photo_label.size()}")

        # Set the restaurant name
        self.parent.restaurant_name_label.setText(self.restaurant_data["name"])
        self.parent.restaurant_name_label.setWordWrap(True)

        # Load and set the restaurant's featured image into self.parent.restaurant_photo_label
        featured_image_url = self.restaurant_data.get("featured_image")  # Adjust the key based on your database schema
        print(f"Featured image URL: {featured_image_url}")  # Debug: Check the image URL

        if featured_image_url:
            if featured_image_url.startswith("http"):  # Check if it's a URL
                try:
                    response = requests.get(featured_image_url)
                    if response.status_code == 200:
                        image_data = QByteArray(response.content)
                        pixmap = QPixmap()
                        pixmap.loadFromData(image_data)
                        print(f"Image loaded from URL: {not pixmap.isNull()}")  # Debug: Check if the image loaded
                    else:
                        print(f"Failed to download image from URL: {featured_image_url}")
                        pixmap = QPixmap()  # Create an empty pixmap if download fails
                except Exception as e:
                    print(f"Error loading image from URL: {e}")
                    pixmap = QPixmap()  # Create an empty pixmap if an error occurs
            else:  # Assume it's a local file path
                pixmap = QPixmap(featured_image_url)
                print(f"Image loaded from local path: {not pixmap.isNull()}")  # Debug: Check if the image loaded

            if not pixmap.isNull():
                # Define the desired size for the circular image (e.g., 100x100 pixels)
                size = 80  # Adjust this to match the desired size of the circular image
                print(f"Original pixmap size: {pixmap.size()}")  # Debug: Check the original size

                # Scale the image to fill the circular area using KeepAspectRatioByExpanding
                scaled_pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                              Qt.TransformationMode.SmoothTransformation)
                print(f"Scaled pixmap size: {scaled_pixmap.size()}")  # Debug: Check the scaled size

                # Crop the scaled pixmap to exactly match the desired size (center the crop)
                width = scaled_pixmap.width()
                height = scaled_pixmap.height()
                x = (width - size) // 2
                y = (height - size) // 2
                cropped_pixmap = scaled_pixmap.copy(x, y, size, size)
                print(f"Cropped pixmap size: {cropped_pixmap.size()}")  # Debug: Check the cropped size

                # Create a circular pixmap using QPainterPath for clipping
                circular_pixmap = QPixmap(size, size)
                circular_pixmap.fill(Qt.GlobalColor.transparent)  # Transparent background
                painter = QPainter(circular_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)

                # Create a circular path for clipping
                path = QPainterPath()
                path.addEllipse(QRectF(0, 0, size, size))
                painter.setClipPath(path)

                # Draw the cropped pixmap
                painter.drawPixmap(0, 0, cropped_pixmap)
                painter.end()

                # Debug: Save the circular pixmap to a file to verify the result
                circular_pixmap.save("debug_circular_image.png", "PNG")
                print("Saved circular pixmap to 'debug_circular_image.png' for debugging")

                # Clear any existing stylesheet to avoid interference
                self.parent.restaurant_photo_label.setStyleSheet("")

                # Set the circular pixmap to the QLabel
                self.parent.restaurant_photo_label.setPixmap(circular_pixmap)
                self.parent.restaurant_photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.parent.restaurant_photo_label.setFixedSize(size, size)  # Ensure the QLabel is the correct size
                self.parent.restaurant_photo_label.setVisible(True)  # Ensure the QLabel is visible
                self.parent.restaurant_photo_label.repaint()  # Force a repaint
                print(
                    f"QLabel size after setting pixmap: {self.parent.restaurant_photo_label.size()}")  # Debug: Check QLabel size
            else:
                print(f"Failed to load image from path/URL: {featured_image_url}")
                self.parent.restaurant_photo_label.setText("No image available")
        else:
            print("No featured image found in restaurant data")
            self.parent.restaurant_photo_label.setText("No image available")


    def setupUi(self):
        import os
        ui_file_path = "ui/menu_page.ui"
        if not os.path.exists(ui_file_path):
            raise FileNotFoundError(f"UI file not found at: {ui_file_path}")
        print(f"Loading UI file from: {ui_file_path}")

        try:
            loadUi(ui_file_path, self)
            print("UI file loaded successfully")
        except Exception as e:
            print(f"Error loading UI file: {e}")
            raise

        self.menu_page = self.findChild(QWidget, "menu_page") or self
        self.menu_page.setVisible(True)
        print(f"menu_page visibility after setting: {self.menu_page.isVisible()}")

        # Table Widget Setup
        table_widget_placeholder = self.findChild(QTableWidget, "tableWidget")
        if table_widget_placeholder is None:
            raise ValueError("tableWidget not found in the UI file.")
        placeholder_layout = table_widget_placeholder.parent().layout()
        placeholder_index = placeholder_layout.indexOf(table_widget_placeholder)
        placeholder_layout.removeWidget(table_widget_placeholder)
        table_widget_placeholder.deleteLater()

        self.tableWidget = MenuDelegate(self.place_id)
        placeholder_layout.insertWidget(placeholder_index, self.tableWidget)
        self.tableWidget.setVisible(True)
        placeholder_layout.parentWidget().setVisible(True)
        print(f"tableWidget visible after setup: {self.tableWidget.isVisible()}")

        self.load_menu_data()
        print("setupUi completed")

    def update_place_id(self, place_id):
        print(f"RestaurantMenuScreen: Updating place_id to {place_id}")
        self.place_id = place_id
        self.menu_model.set_place_id(place_id)
        self.tableWidget.place_id = place_id
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.load_menu_data()

    def load_menu_data(self):
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
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            menu_items = self.menu_model.get_menu(use_pagination=False)  # Lấy toàn bộ dữ liệu

            print(f"Loaded menu items: {len(menu_items)} items")
            print(f"Menu items: {menu_items}")

            if not menu_items:
                print("No menu items to display.")
                self.tableWidget.clearContents()
                self.tableWidget.setRowCount(1)
                item = QtWidgets.QTableWidgetItem("No menu items available for this restaurant.")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(0, 0, item)
                return

            self.tableWidget.load_more_menu(menu_items)
            self.tableWidget.update()
            self.tableWidget.repaint()
            print(f"Total rows in table after load: {self.tableWidget.rowCount()}")
            print(f"Table widget visible: {self.tableWidget.isVisible()}")
            print(f"menu_page visible: {self.menu_page.isVisible()}")
        except AttributeError as e:
            print(f"Error in load_menu_data: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error in load_menu_data: {e}")
            raise

    def on_slotDelegate_byrow(self, item):
        row = item.row()
        product_id = self.tableWidget.item(row, 0).text()
        item_name = self.tableWidget.item(row, 2).text()
        print(f"Selected menu item: product_id={product_id}, name={item_name}")

    def closeEvent(self, event):
        print("Closing RestaurantMenuScreen")
        self.menu_model.close_connection()
        if self.tableWidget:
            self.tableWidget.close()
        event.accept()
        print("RestaurantMenuScreen closed")