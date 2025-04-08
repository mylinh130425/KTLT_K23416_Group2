import requests
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QByteArray, QRectF
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget, QTableWidget, QPushButton, QLabel, QStackedWidget
from PyQt6.uic import loadUi
from project.src.delegate.MenuDelegate import MenuDelegate
from project.src.model.MenuModel import MenuModel
from project.src.DatabaseManager import DatabaseManager
from bson import ObjectId

class RestaurantMenuScreen(QWidget):
    IMAGE_SIZE = 80
    ROW_HEIGHT = 130

    def __init__(self, place_id, parent=None):
        super().__init__(parent)
        self.place_id = place_id
        self.parent = parent
        self.menu_model = MenuModel(place_id)
        self.db_manager = DatabaseManager()
        print(f"RestaurantMenuScreen: Place ID used: {self.place_id}")
        self.restaurant_name = self.fetch_restaurant_name()
        self.setupUi()

    def fetch_restaurant_name(self):
        if not self.place_id:
            print("fetch_restaurant_name: place_id is None, cannot fetch restaurant name")
            return "Unknown Restaurant"

        try:
            place_id_obj = ObjectId(self.place_id)
            print(f"Converted place_id to ObjectId: {place_id_obj}")

            print(f"Querying Menu collection with place_id: {place_id_obj}")
            menu_doc = self.db_manager.db["Menu"].find_one({"place_id": place_id_obj})
            if menu_doc:
                print(f"Found menu document: {menu_doc}")
                restaurant_name = menu_doc.get("restaurant_name")
                if restaurant_name:
                    print(f"Fetched restaurant name from Menu collection: {restaurant_name}")
                    return restaurant_name
                else:
                    print("No restaurant_name field found in Menu document")
            else:
                print(f"No menu document found for place_id: {place_id_obj} in Menu collection")

            print(f"Querying Restaurants collection with place_id: {place_id_obj}")
            restaurant = self.db_manager.db["Restaurants"].find_one({"place_id": place_id_obj})
            if restaurant:
                print(f"Found restaurant document: {restaurant}")
                name = restaurant.get("name") or restaurant.get("restaurant_name") or "Unknown Restaurant"
                print(f"Fetched restaurant name from Restaurants collection: {name}")
                return name
            else:
                print(f"No restaurant found for place_id: {place_id_obj} in Restaurants collection")

            menu_items = self.menu_model.get_menu(use_pagination=False)
            print(f"Menu items for inference: {menu_items}")
            if menu_items:
                for item in menu_items:
                    description = item.get("Description", "")
                    if "Vincom Thủ Đức" in description:
                        inferred_name = "Gỏi House Vincom Thủ Đức"
                        print(f"Inferred restaurant name from menu item description: {inferred_name}")
                        return inferred_name
            print("Could not infer restaurant name from menu items")
            return "Unknown Restaurant"
        except Exception as e:
            print(f"Error fetching restaurant name: {e}")
            return "Unknown Restaurant"

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

        # Restaurant Name Label
        # self.restaurant_name_label = self.parent.findChild(QLabel, "restaurant_name_label")
        self.restaurant_name_label = self.parent.restaurant_name_label
        try:
            if self.restaurant_name_label is None:
                raise ValueError("restaurant_name_label not found in the UI file.")
        except Exception as e:
            print(e)
        self.restaurant_name_label.setText(self.restaurant_name)
        self.restaurant_name_label.setWordWrap(True)
        self.restaurant_name_label.setStyleSheet(
            "color: #FABC3F; font-size: 20px; font-weight: bold; background-color: #343131;")
        self.restaurant_name_label.setMinimumSize(200, 30)
        self.restaurant_name_label.setMaximumSize(16777215, 50)
        self.restaurant_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.restaurant_name_label.setVisible(True)
        print(f"restaurant_name_label text: '{self.restaurant_name_label.text()}'")
        print(f"restaurant_name_label visible: {self.restaurant_name_label.isVisible()}")

        # Restaurant Photo Label (Circular Image)
        self.restaurant_photo_label = self.findChild(QLabel, "restaurant_photo_label")
        if self.restaurant_photo_label is None:
            print("restaurant_photo_label not found in UI file!")
        else:
            featured_image_url = self.db_manager.get_restaurant_byid(self.place_id).get("featured_image")
            print(f"Image URL: {featured_image_url}")
            if featured_image_url and featured_image_url.startswith("http"):
                try:
                    response = requests.get(featured_image_url)
                    if response.status_code == 200:
                        pixmap = QPixmap()
                        pixmap.loadFromData(QByteArray(response.content))
                        if not pixmap.isNull():
                            # Define size for circular image
                            size = 90  # Adjust as needed

                            # Scale image, keeping aspect ratio, expanding to fill
                            scaled_pixmap = pixmap.scaled(
                                size, size,
                                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                Qt.TransformationMode.SmoothTransformation
                            )
                            print(f"Scaled pixmap size: {scaled_pixmap.size()}")

                            # Crop to square (center the crop)
                            width = scaled_pixmap.width()
                            height = scaled_pixmap.height()
                            x = (width - size) // 2
                            y = (height - size) // 2
                            cropped_pixmap = scaled_pixmap.copy(x, y, size, size)

                            # Create circular pixmap
                            circular_pixmap = QPixmap(size, size)
                            circular_pixmap.fill(Qt.GlobalColor.transparent)
                            painter = QPainter(circular_pixmap)
                            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                            path = QPainterPath()
                            path.addEllipse(QRectF(0, 0, size, size))
                            painter.setClipPath(path)
                            painter.drawPixmap(0, 0, cropped_pixmap)
                            painter.end()

                            # Debug: Save to verify
                            circular_pixmap.save("debug_circular_image.png", "PNG")
                            print("Saved circular image to 'debug_circular_image.png'")

                            # Set to label
                            self.restaurant_photo_label.setPixmap(circular_pixmap)
                            self.restaurant_photo_label.setFixedSize(size, size)
                            self.restaurant_photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            self.restaurant_photo_label.setStyleSheet("border: none; background: transparent;")
                            self.restaurant_photo_label.setVisible(True)
                            print(f"Photo label size: {self.restaurant_photo_label.size()}")
                        else:
                            print("Failed to load image data")
                            self.restaurant_photo_label.setText("No image")
                    else:
                        print(f"Image request failed: {response.status_code}")
                        self.restaurant_photo_label.setText("No image")
                except Exception as e:
                    print(f"Image load error: {e}")
                    self.restaurant_photo_label.setText("No image")
            else:
                print("No valid image URL found")
                self.restaurant_photo_label.setText("No image")
            self.restaurant_photo_label.repaint()

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
        self.restaurant_name = self.fetch_restaurant_name()
        self.restaurant_name_label.setText(self.restaurant_name)
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