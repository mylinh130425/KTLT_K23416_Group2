from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6 import QtWidgets, QtGui, QtCore
from project.src.delegate.RestaurantDelegate import RestaurantDelegate
from project.src.view.RestaurantMenuScreen import RestaurantMenuScreen
from project.src.view.AllMenuItemScreen import AllMenuItemScreen

class RestaurantScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tableWidget = None
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

        # SpacerItem để đẩy các nút về bên phải
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
        self.restaurant_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.restaurant_table.cellDoubleClicked.connect(self.open_menu_screen)

        # Kiểm tra các sự kiện khác có thể gây nhầm lẫn
        self.restaurant_table.itemClicked.connect(self.on_item_clicked)

        # Thêm bảng vào layout chính
        layout.addWidget(self.restaurant_table)

        # Set layout cho QWidget
        self.setLayout(layout)

    def on_scroll(self):
        """Tải thêm dữ liệu khi cuộn xuống cuối."""
        scrollbar = self.restaurant_table.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum():
            self.restaurant_table.load_more_restaurants()

    def on_item_clicked(self, item):
        """Kiểm tra xem itemClicked có bị gọi không."""
        print(f"RestaurantScreen: Item clicked at row {item.row()}, column {item.column()}")

    def open_menu_screen(self, row, column):
        """Mở trang menu khi double-click vào nhà hàng."""
        print(f"RestaurantScreen: Double-clicked at row {row}, column {column}")
        place_id_item = self.restaurant_table.item(row, 0)
        if place_id_item is None:
            restaurant_data = self.restaurant_table.model.get_restaurants()[row]
            print(f"RestaurantScreen: No place_id found for row {row}, restaurant_data: {restaurant_data}")
            return

        place_id = place_id_item.text()
        if not place_id:
            print(f"RestaurantScreen: place_id is empty at row {row}")
            return

        print(f"RestaurantScreen: Selected place_id: {place_id}")
        print(f"Parent objectName: {self.parent.objectName()}")
        # Gọi show_menu_for_restaurant() thay vì tạo mới RestaurantMenuScreen
        self.parent.show_menu_for_restaurant(place_id)

    def open_all_menu_screen(self):
        """Mở trang hiển thị tất cả menu."""
        print(f"RestaurantScreen: Opening AllMenuItemScreen")
        print(f"Parent objectName: {self.parent.objectName()}")
        self.parent.body_stackedWidget.all_menu_page = AllMenuItemScreen(self.parent)
        self.parent.body_stackedWidget.setCurrentWidget(self.parent.inside_restaurant_page)
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.body_stackedWidget.all_menu_page)

    def on_double_click(self, item):
        row = item.row()
        place_id = self.tableWidget.item(row, 0).text()  # Lấy place_id từ cột "_id"
        print(f"RestaurantScreen: Double-clicked on place_id: {place_id}")
        if self.parent:
            self.parent.show_menu_for_restaurant(place_id)