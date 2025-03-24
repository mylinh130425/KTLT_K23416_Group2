from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6 import QtWidgets, QtGui,QtCore

from project.src.delegate.RestaurantDelegate import RestaurantDelegate
from project.src.view.RestaurantMenuScreen import RestaurantMenuScreen


class RestaurantScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setupUi()

    def setupUi(self):

        layout = QVBoxLayout(self)

        # Layout chứa các nút điều khiển (Filter, Create, Edit, Delete)
        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(10, 10, 10, 10)
        buttonLayout.setSpacing(10)

        # Nút Filter (Góc trái)
        self.filter_pushButton = QPushButton(parent=self.parent.body_stackedWidget)
        self.filter_pushButton.setText("Filter")
        filter_icon = QtGui.QIcon(":/images/ic_adjust.png")
        self.filter_pushButton.setIcon(filter_icon)
        self.filter_pushButton.setIconSize(QtCore.QSize(15, 15))
        self.filter_pushButton.setObjectName("filter_pushButton")
        buttonLayout.addWidget(self.filter_pushButton)

        # SpacerItem để đẩy 3 nút Create, Edit, Delete về bên phải
        buttonLayout.addStretch()

        # Nút Create
        self.create_pushButton = QPushButton("Create", parent=self.parent.body_stackedWidget)
        self.create_pushButton.setObjectName("create_pushButton")
        buttonLayout.addWidget(self.create_pushButton)

        # Nút Edit
        self.edit_pushButton = QPushButton("Edit", parent=self.parent.body_stackedWidget)
        self.edit_pushButton.setObjectName("edit_pushButton")
        buttonLayout.addWidget(self.edit_pushButton)

        # Nút Delete
        self.delete_pushButton = QPushButton("Delete", parent=self.parent.body_stackedWidget)
        self.delete_pushButton.setObjectName("delete_pushButton")
        buttonLayout.addWidget(self.delete_pushButton)

        # Thêm hàng nút vào layout chính
        layout.addLayout(buttonLayout)

        # Bảng RestaurantDelegate (QTableWidget)
        self.restaurant_table = RestaurantDelegate()
        self.restaurant_table.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.restaurant_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)  # Disable editing
        self.restaurant_table.cellDoubleClicked.connect(self.open_menu_screen)

        # Thêm bảng vào layout chính
        layout.addWidget(self.restaurant_table)

        # Set layout cho QWidget
        self.setLayout(layout)


    def on_scroll(self):
        """Tải thêm dữ liệu khi cuộn xuống cuối."""
        scrollbar = self.restaurant_table.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum():
            self.restaurant_table.load_more_restaurants()
    def open_menu_screen(self, row):
        """Mở trang menu khi double-click vào nhà hàng."""
        place_id = self.restaurant_table.item(row, 0).text()  # Lấy ID nhà hàng
        # print(place_id)
        print(self.parent.objectName())
        self.parent.body_stackedWidget.menu_page = RestaurantMenuScreen(place_id, self.parent)
        self.parent.body_stackedWidget.setCurrentWidget(self.parent.inside_restaurant_page)
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.menu_page)
        #rồi set cái stacked widget bên trong vào đúng trang menu_page

