# from PyQt6.QtGui import QPixmap
from PyQt6 import QtWidgets, QtGui,QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QDialog, QLineEdit, QLabel, \
    QDialogButtonBox
from project.src.delegate.RestaurantDelegate import RestaurantDelegate
from project.src.filter_restaurant import MongoDBConnection, filter_restaurants
from project.src.view.ModifyRestaurantScreen import ModifyRestaurantScreen
from project.src.view.RestaurantMenuScreen import RestaurantMenuScreen
from project.src.view.AllMenuItemScreen import AllMenuItemScreen

class RestaurantScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tableWidget = None
        self.parent = parent
        self.current_restaurant_id=None
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
        filter_icon = QtGui.QIcon(":/MealMatch/Icons/MealMatch/ic_filter24.png")
        self.filter_pushButton.setIcon(filter_icon)
        self.filter_pushButton.setIconSize(QtCore.QSize(15, 15))
        self.filter_pushButton.setObjectName("filter_pushButton")
        self.filter_pushButton.setStyleSheet("color: #FABC3F;background-color: #343131; padding-left: 15px;padding-right: 15px;")
        buttonLayout.addWidget(self.filter_pushButton)

        # Kết nối sự kiện clicked của nút Filter
        self.filter_pushButton.clicked.connect(self.filter_restaurants_by_criteria)

        # SpacerItem để đẩy các nút về bên phải
        buttonLayout.addStretch()

        buttonLayout.setSpacing(10)
        # Nút Create
        self.create_pushButton = QPushButton("Create", parent=self.parent.body_stackedWidget)
        self.create_pushButton.setObjectName("create_pushButton")
        buttonLayout.addWidget(self.create_pushButton)
        self.create_pushButton.setStyleSheet("color: #FABC3F;background-color: #343131; padding-left: 15px;padding-right: 15px;")
        self.create_pushButton.clicked.connect(self.goAddRestaurant)

        # Nút Edit
        self.edit_pushButton = QPushButton("Edit", parent=self.parent.body_stackedWidget)
        self.edit_pushButton.setObjectName("edit_pushButton")
        self.edit_pushButton.setStyleSheet("color: #FABC3F;background-color: #343131; padding-left: 15px;padding-right: 15px;")
        buttonLayout.addWidget(self.edit_pushButton)
        self.edit_pushButton.clicked.connect(self.goEditRestaurant)

        # Nút Delete
        self.delete_pushButton = QPushButton("Delete", parent=self.parent.body_stackedWidget)
        self.delete_pushButton.setObjectName("delete_pushButton")
        buttonLayout.addWidget(self.delete_pushButton)
        self.delete_pushButton.setStyleSheet("color: #FABC3F;background-color: #343131; padding-left: 15px;padding-right: 15px;")
        self.delete_pushButton.clicked.connect(self.deleteRestaurant)

        # Thêm hàng nút vào layout chính
        layout.addLayout(buttonLayout)

        # Bảng RestaurantDelegate (QTableWidget)
        self.restaurant_table = RestaurantDelegate()
        self.restaurant_table.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.restaurant_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.restaurant_table.cellDoubleClicked.connect(self.open_menu_screen)
        self.restaurant_table.itemClicked.connect(self.on_item_clicked)

        # Thêm bảng vào layout chính
        layout.addWidget(self.restaurant_table)

        # Set layout cho QWidget
        self.setLayout(layout)

        #add event to track stackedwidget change
        # self.parent.body_stackedWidget.currentChanged.connect(self.onStackedWidgetChanged)

    # def onStackedWidgetChanged(self, index):
    #     """ Event handler for stacked widget page changes. """
    #
    #     print("stackedwidgetchanged")
    #     # Ensure we're switching to the modify restaurant page
    #     current_page =self.parent.body_stackedWidget.widget(index)
    #     print(current_page.objectName())
    #     if current_page.objectName() == self.parent.inside_restaurant_page.objectName():
    #
    #         selected_items = self.restaurant_table.selectedItems()
    #
    #         if len(selected_items)==0:  # No row selected
    #             self.parent.body_stackedWidget.setCurrentWidget(self.parent.restaurant_page)
    #             QMessageBox.warning(self, "Selection Error", "Please select a restaurant first!")
    #             return
    #         ModifyRestaurantScreen(self.parent, isCreating=False, restaurant_id=self.current_restaurant_id)
    #
    #         # Get the selected restaurant's ID (assuming it's in column 0)
    #         selected_row = selected_items[0].row()
    #         self.current_restaurant_id = self.restaurant_table.item(selected_row, 0).text()
    #         restaurant_name = self.restaurant_table.item(selected_row, 2).text()
    #
    #
    #         print("setting up restaurant name", restaurant_name)
    #         self.parent.restaurant_name_label.setText(restaurant_name)
    #         self.parent.restaurant_name_label.setWordWrap(True)
    # def goAddRestaurant(self):
    #     """ Navigate to the Add Restaurant screen. """
    #     print("Navigating to Add Restaurant screen")
    #     ModifyRestaurantScreen(self.parent, isCreating=True)

    def filter_restaurants_by_criteria(self):
        """Mở dialog để lọc nhà hàng theo rating và tên"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Filter Restaurants")
        layout = QVBoxLayout(dialog)

        # Ô nhập rating tối thiểu
        rating_input = QLineEdit()
        rating_input.setPlaceholderText("Enter minimum rating (e.g., 3.5)")
        layout.addWidget(QLabel("Minimum Rating:"))
        layout.addWidget(rating_input)

        # Ô nhập tên nhà hàng
        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter restaurant name (e.g., Pizza Hut)")
        layout.addWidget(QLabel("Restaurant Name:"))
        layout.addWidget(name_input)

        # Nút OK và Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec():
            # Lấy giá trị từ các ô nhập
            min_rating = None
            try:
                if rating_input.text():
                    min_rating = float(rating_input.text())
                    if min_rating < 0 or min_rating > 5:
                        QMessageBox.warning(self, "Error", "Rating must be between 0 and 5.")
                        return
            except ValueError:
                QMessageBox.warning(self, "Error", "Please enter a valid number for rating.")
                return

            name = name_input.text() if name_input.text() else None

            # Gọi filter_restaurants để lấy danh sách nhà hàng đã lọc
            filtered_restaurants = filter_restaurants(
                min_rating=min_rating,
                name=name,
                limit=10
            )

            # Cập nhật bảng với kết quả lọc
            if filtered_restaurants:
                self.restaurant_table.load_more_restaurants(filtered_restaurants)  # Truyền danh sách đã lọc
                QMessageBox.information(self, "Success", f"Found {len(filtered_restaurants)} restaurants matching the criteria.")
            else:
                self.restaurant_table.load_more_restaurants([])  # Truyền danh sách rỗng để hiển thị thông báo "No restaurants match the filter criteria."
                QMessageBox.information(self, "Info", "No restaurants found matching the criteria.")

    def goEditRestaurant(self):
        """ Navigate to Edit Restaurant screen (must have a selected row). """
        selected_items = self.restaurant_table.selectedItems()

        if len(selected_items)==0:
            QMessageBox.warning(self, "Selection Error", "Please select a restaurant first!")
            return

        selected_row = selected_items[0].row()
        self.current_restaurant_id = self.restaurant_table.item(selected_row, 0).text()
        restaurant_name = self.restaurant_table.item(selected_row, 2).text()

        print("Editing restaurant:", restaurant_name)
        print("parent", self.parent.inside_restaurant_page)
        # self.parent.restaurant_name_label.setText(restaurant_name)
        # self.parent.restaurant_name_label.setWordWrap(True)


        self.parent.body_stackedWidget.setCurrentWidget(self.parent.inside_restaurant_page)
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.modify_restaurant_page)
        #create a new variable in MainWindow to store ModifyRestaurantScreen object
        # for manipulating the modify_restaurant_page
        self.parent.modify_restaurant= ModifyRestaurantScreen(self.parent, isCreating=False, restaurant_id=self.current_restaurant_id)


    def goInfoRestaurant(self, row):
        """ Navigate to restaurant info screen on double click. """
        self.current_restaurant_id = self.restaurant_table.item(row, 0).text()
        restaurant_name = self.restaurant_table.item(row, 2).text()

        print("Viewing restaurant info:", restaurant_name)
        self.parent.restaurant_name_label.setText(restaurant_name)
        self.parent.restaurant_name_label.setWordWrap(True)

        self.parent.body_stackedWidget.setCurrentWidget(self.parent.inside_restaurant_page)

    def goAddRestaurant(self):
        self.parent.body_stackedWidget.setCurrentWidget(self.parent.inside_restaurant_page)
        self.modifyRestaurantScreen = ModifyRestaurantScreen(self.parent, isCreating=True)
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.add_restaurant_page)

    def setupRestaurantInfo(self):
        modify_restaurant_screen = ModifyRestaurantScreen(self.parent, isCreating=False) #parent: Extend_Mainwindow

    def deleteRestaurant(self):
        """ Navigate to Edit Restaurant screen (must have a selected row). """
        selected_items = self.restaurant_table.selectedItems()

        if len(selected_items)==0:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a restaurant to delete.")
            return

        selected_row = selected_items[0].row()
        self.current_restaurant_id = self.restaurant_table.item(selected_row, 0).text()
        restaurant_name = self.restaurant_table.item(selected_row, 2).text()

        print("Deleting ", self.current_restaurant_id, restaurant_name)
        if not self.current_restaurant_id or not restaurant_name:
            QtWidgets.QMessageBox.warning(self, "Error", "Could not retrieve restaurant data.")
            return


        # Confirm deletion
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{restaurant_name}'?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            # Delete from database
            success = self.restaurant_table.delete_restaurant_by_id(self.current_restaurant_id )
            if success:
                self.restaurant_table.removeRow(selected_row)
                QtWidgets.QMessageBox.information(self, "Deleted",
                                                  f"Restaurant '{restaurant_name}' was deleted successfully.")
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to delete the restaurant.")

    def on_scroll(self):
        """Tải thêm dữ liệu khi cuộn xuống cuối, nhưng không tải nếu đang ở trạng thái lọc."""
        scrollbar = self.restaurant_table.verticalScrollBar()
        if scrollbar.value() == scrollbar.maximum() and not self.restaurant_table.is_filtered:
            self.restaurant_table.load_more_restaurants()

    def on_item_clicked(self, item):
        """Kiểm tra xem itemClicked có bị gọi không."""
        print(f"RestaurantScreen: Item clicked at row {item.row()}, column {item.column()}")

    def open_menu_screen(self, row, column):
        """Mở trang menu khi double-click vào nhà hàng."""
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
        # place_id = self.restaurant_table.item(row, 0).text()  # Lấy ID nhà hàng
        # print(place_id)
        # print(self.parent.objectName())
        self.parent.restaurant_stackedWidget.menu_page = RestaurantMenuScreen(place_id=None, parent = self.parent)
        self.parent.body_stackedWidget.setCurrentWidget(self.parent.inside_restaurant_page)
        self.parent.restaurant_stackedWidget.setCurrentWidget(self.parent.body_stackedWidget.all_menu_page)

