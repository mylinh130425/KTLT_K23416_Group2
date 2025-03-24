from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6 import QtWidgets, QtGui,QtCore

from project.src.delegate.RestaurantDelegate import RestaurantDelegate
from project.src.view.ModifyRestaurantScreen import ModifyRestaurantScreen
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
        self.create_pushButton.clicked.connect(self.goAddRestaurant)

        # Nút Edit
        self.edit_pushButton = QPushButton("Edit", parent=self.parent.body_stackedWidget)
        self.edit_pushButton.setObjectName("edit_pushButton")
        buttonLayout.addWidget(self.edit_pushButton)
        self.edit_pushButton.clicked.connect(self.goEditRestaurant)

        # Nút Delete
        self.delete_pushButton = QPushButton("Delete", parent=self.parent.body_stackedWidget)
        self.delete_pushButton.setObjectName("delete_pushButton")
        buttonLayout.addWidget(self.delete_pushButton)
        self.delete_pushButton.clicked.connect(self.deleteRestaurant)

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
    def goAddRestaurant(self):
        self.parent.body_stackedWidget.setCurrentWidget(self.parent.inside_restaurant_page)
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.add_restaurant_page)
        add_restaurant_screen = ModifyRestaurantScreen(self.parent, isCreating=True)


    def goEditRestaurant(self):
        modify_restaurant_screen = ModifyRestaurantScreen(self.parent, isCreating=False)
        self.parent.body_stackedWidget.setCurrentWidget(self.parent.inside_restaurant_page)
        self.parent.body_stackedWidget.setCurrentWidget(self.parent.modify_food_page)

    def deleteRestaurant(self):
        selected_items = self.restaurant_table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a restaurant to delete.")
            return

        selected_row = selected_items[0].row()
        place_id_item = self.restaurant_table.item(selected_row, 0)
        restaurant_name_item = self.restaurant_table.item(selected_row, 1)

        if not place_id_item or not restaurant_name_item:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve restaurant data.")
            return

        place_id = place_id_item.text()
        restaurant_name = restaurant_name_item.text()

        # Confirm deletion
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{restaurant_name}'?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            # Delete from database
            success = self.restaurant_table.delete_restaurant_by_id(place_id)
            if success:
                self.restaurant_table.removeRow(selected_row)
                QtWidgets.QMessageBox.information(self, "Deleted",
                                                  f"Restaurant '{restaurant_name}' was deleted successfully.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to delete the restaurant.")

    def on_scroll(self):
        """Tải thêm dữ liệu khi cuộn xuống cuối."""
        scrollbar = self.restaurant_table.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum():
            self.restaurant_table.load_more_restaurants()
    def open_menu_screen(self, row):
        """Mở trang menu khi double-click vào nhà hàng."""
        place_id = self.restaurant_table.item(row, 0).text()  # Lấy ID nhà hàng
        # print(place_id)
        # print(self.parent.objectName())
        self.parent.body_stackedWidget.menu_page = RestaurantMenuScreen(place_id, self.parent)
        self.parent.body_stackedWidget.setCurrentWidget(self.parent.inside_restaurant_page)
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.menu_page)

        #setup buttons on restaurant side bar
        self.name = self.parent.restaurant_table.item(row, 2).text()
        self.parent.restaurant_name_label.setText(self.name)
        self.parent.restaurant_info_button.clicked.connect(self.goInfo)
        self.parent.restaurant_menu_button.clicked.connect(self.goMenu)
        self.parent.restaurant_review_button.clicked.connect(self.goReview)

    def goInfo(self):
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.modify_restaurant_page)
    def goMenu(self):
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.menu_page)
    def goReview(self):
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.review_restaurant_page)

