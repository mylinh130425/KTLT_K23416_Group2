from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from project.src.delegate.MenuDelegate import MenuDelegate
from project.src.model.MenuModel import MenuModel

class AllMenuItemScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.menu_model = MenuModel()
        print("AllMenuItemScreen: Initialized")
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

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

        layout.addLayout(button_layout)

        self.tableWidget = MenuDelegate()
        self.tableWidget.setObjectName("tableWidget")
        layout.addWidget(self.tableWidget)

        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget.verticalScrollBar().valueChanged.connect(self.on_scroll)

        self.load_menu_data()

    def load_menu_data(self):
        try:
            print("AllMenuItemScreen: Loading all menu items")
            menu_items = self.menu_model.get_all_menus(use_pagination=True)

            print(f"AllMenuItemScreen: Loaded menu items (initial load): {len(menu_items)} items")
            print(f"AllMenuItemScreen: Menu items: {menu_items}")

            if not menu_items:
                print("AllMenuItemScreen: No menu items to display.")
                self.tableWidget.clearContents()
                self.tableWidget.setRowCount(1)
                item = QtWidgets.QTableWidgetItem("No menu items available.")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(0, 0, item)
                return

            self.tableWidget.load_more_menu(menu_items)
            self.tableWidget.update()
            self.tableWidget.repaint()
            print(f"AllMenuItemScreen: Total rows in table after initial load: {self.tableWidget.rowCount()}")
        except AttributeError as e:
            print(f"AllMenuItemScreen: Error in load_menu_data: {e}")

    def on_scroll(self):
        scroll_bar = self.tableWidget.verticalScrollBar()
        if scroll_bar.value() >= scroll_bar.maximum() - 10:
            print("AllMenuItemScreen: Reached near end of scroll, loading more menu items...")
            menu_items = self.menu_model.get_all_menus(use_pagination=True)

            print(f"AllMenuItemScreen: Loaded additional menu items: {len(menu_items)} items")
            print(f"AllMenuItemScreen: Additional menu items: {menu_items}")

            if menu_items:
                self.tableWidget.load_more_menu(menu_items)
                print(f"AllMenuItemScreen: Total rows in table after loading more: {self.tableWidget.rowCount()}")
            else:
                print("AllMenuItemScreen: No more menu items to load.")

    def closeEvent(self, event):
        self.menu_model.close_connection()
        event.accept()