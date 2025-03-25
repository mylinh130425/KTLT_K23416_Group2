from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from project.src.delegate.MenuDelegate import MenuDelegate
from project.src.model.MenuModel import MenuModel

class RestaurantMenuScreen(QWidget):
    IMAGE_SIZE = 80
    ROW_HEIGHT = 130

    def __init__(self, place_id=None, parent=None):
        super().__init__(parent)
        self.place_id = place_id
        self.parent = parent
        self.menu_model = MenuModel(place_id)

        #get restaurant data for name and featured image
        self.restaurant_data = self.parent.db_manager.get_restaurant_byid(place_id)
        print(self.restaurant_data)
        print(f"RestaurantMenuScreen: Place ID used: {self.place_id}")
        if self.place_id is None:
            self.setupUi()
        else:
            self.updateUi()

    def updateUi(self):
        self.parent.restaurant_name_label.setText(self.restaurant_data["name"])
        self.parent.restaurant_name_label.setWordWrap(True)
        #replace menupage_tableWidget designed in QtDesigner with MenuDelegate
        self.parent.menu_verticalLayout.removeWidget(self.parent.menupage_tableWidget)
        self.parent.menupage_tableWidget = MenuDelegate(self.place_id)
        self.parent.menupage_tableWidget.setObjectName("menupage_tableWidget")
        self.tableWidget = self.parent.menupage_tableWidget
        self.tableWidget.setObjectName("menu")
        self.parent.menu_verticalLayout.addWidget(self.tableWidget)

        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.on_scroll)

        self.tableWidget.itemClicked.connect(self.on_slotDelegate_byrow)
        self.load_menu_data()
        #signals and slots
        self.parent.menupage_filter_button.clicked.connect(self.filter_menu)
        self.parent.menupage_create_button.clicked.connect(self.create_menu)
        self.parent.menupage_edit_button.clicked.connect(self.edit_menu)
        self.parent.menupage_delete_button.clicked.connect(self.delete_menu)

    def filter_menu(self):
        pass
    def create_menu(self):
        pass
    def edit_menu(self):
        pass
    def delete_menu(self):
        pass

    def setupUi(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)
        button_layout.setSpacing(10)

        self.filter_pushButton = QPushButton()
        self.filter_pushButton.setText("Filter")
        filter_icon = QIcon(":/images/ic_adjust.png")
        self.filter_pushButton.setIcon(filter_icon)
        self.filter_pushButton.setIconSize(QtCore.QSize(15, 15))
        self.filter_pushButton.setObjectName("filter_pushButton")
        button_layout.addWidget(self.filter_pushButton)

        button_layout.addStretch()

        self.create_pushButton = QPushButton("Create")
        self.create_pushButton.setObjectName("create_pushButton")
        button_layout.addWidget(self.create_pushButton)

        self.edit_pushButton = QPushButton("Edit")
        self.edit_pushButton.setObjectName("edit_pushButton")
        button_layout.addWidget(self.edit_pushButton)

        self.delete_pushButton = QPushButton("Delete")
        self.delete_pushButton.setObjectName("delete_pushButton")
        button_layout.addWidget(self.delete_pushButton)

        self.main_layout.addLayout(button_layout)

        self.tableWidget = MenuDelegate(self.place_id)
        self.tableWidget.setObjectName("tableWidget")
        self.main_layout.addWidget(self.tableWidget)

        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.on_scroll)

        self.tableWidget.itemClicked.connect(self.on_slotDelegate_byrow)

        self.load_menu_data()

    def update_place_id(self, place_id):
        """Cập nhật place_id và tải lại dữ liệu menu."""
        print(f"RestaurantMenuScreen: Updating place_id to {place_id}")
        self.place_id = place_id
        self.menu_model.set_place_id(place_id)  # Cập nhật place_id và reset offset
        self.tableWidget.place_id = place_id
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.load_menu_data()

    def load_menu_data(self):
        print("loading menu for restaurant", self.place_id)
        try:
            if self.place_id is None:
                print("load_menu_data: place_id is None, cannot load menu")
                self.tableWidget.clearContents()
                self.tableWidget.setRowCount(1)
                item = QtWidgets.QTableWidgetItem("No place_id provided.")
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

    def on_scroll(self):
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
        row = item.row()
        product_id = self.tableWidget.item(row, 0).text()
        item_name = self.tableWidget.item(row, 2).text()
        print(f"Selected menu item: product_id={product_id}, name={item_name}")

    def closeEvent(self, event):
        self.menu_model.close_connection()
        event.accept()