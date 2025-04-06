from pathlib import Path

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox, QFrame, QVBoxLayout, QPushButton, QDockWidget, QMainWindow, QListWidgetItem, \
    QListWidget, QWidget
from PyQt6.QtCore import Qt, QSize
from project.src.DatabaseManager import DatabaseManager
from project.src.model.ProfileModel import ProfileModel
from project.src.view.AllMenuItemScreen import AllMenuItemScreen
from project.src.view.RestaurantMenuScreen import RestaurantMenuScreen
from project.src.view.RestaurantScreen import RestaurantScreen
from project.src.view.ProfileScreen import ProfileScreen
from project.src.ui_interface_stacked import *

class Extend_MainWindow(QMainWindow, Ui_MainWindow):
    def setupUi(self, MainWindow):
        print("Starting setupUi")
        super().setupUi(MainWindow)
        self.width = MainWindow.width()
        self.height = MainWindow.height()
        self.setFixedSize(self.width, self.height)
        self.db_manager = DatabaseManager()
        self.username = None
        self.fullname = None
        self.profile = None

        # print("Setting up pages")
        # self.setup_pages()

        print("Setting current widget to Login_SignUp")
        self.stackedWidget.setCurrentWidget(self.Login_SignUp)
        self.login_signup_stackedWidget.setCurrentWidget(self.right_login_page)
        print("Setting up menu burger")
        self.setup_menuburger()
        print("Processing signals and slots")
        self.processSignalAndSlot()
        print("Finished setupUi")

        # Đường dẫn tuyệt đối đến ảnh
        absolute_path_welcome = Path("../project/image/CreateAcc_Image.png").resolve()
        absolute_path_profile = Path("../project/image/Account-amico 1.png").resolve()
        # Kiểm tra và load ảnh vào QLabel
        if absolute_path_welcome.exists():
            pixmap_welcome = QPixmap(str(absolute_path_welcome)).scaled(
                300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            self.welcome_photo.setPixmap(pixmap_welcome)
        else:
            print(f"Lỗi: Không tìm thấy ảnh {absolute_path_welcome}")
        if absolute_path_profile.exists():
            pixmap_profile = QPixmap(str(absolute_path_profile)).scaled(
                300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            self.label.setPixmap(pixmap_profile)
        else:
            print(f"Lỗi: Không tìm thấy ảnh {absolute_path_profile}")

    def processSignalAndSlot(self):
        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.signup)
        self.to_login_button.clicked.connect(self.goLogin)
        self.to_signup_button.clicked.connect(self.goSignUp)
        self.home_button.clicked.connect(self.goHome)
        self.profile_logout_button.clicked.connect(self.logout)
        self.profile_save_button.clicked.connect(self.updateProfile)
        self.profile_delete_button.clicked.connect(self.deleteProfile)
        self.burger_menu_button.clicked.connect(self.toggle_menu)
        self.centralwidget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.MouseButtonPress:
            if self.menu_dock.isVisible():
                if not self.menu_dock.geometry().contains(event.globalPosition().toPoint()):
                    self.menu_dock.setVisible(False)
                    return True
        return super().eventFilter(obj, event)

    def deleteProfile(self):
        reply = QMessageBox.question(
            self.body_stackedWidget,
            "Confirm Deletion",
            "Are you sure you want to delete your profile? This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.stackedWidget.setCurrentWidget(self.Login_SignUp)
            self.goSignUp()
            success = self.profile.delete_profile(self.username)
            if success:
                QMessageBox.information(self.body_stackedWidget, "Success", "Your profile has been deleted successfully.")
                self.username = None
            else:
                QMessageBox.critical(self.body_stackedWidget, "Error", "Failed to delete your profile. Please try again.")

    def updateProfile(self):
        old_username = self.username
        new_username = self.profile_username_lineEdit.text().strip()
        new_fullname = self.profile_fullname_lineEdit.text().strip()
        current_password = self.profile_currentpassword_lineEdit.text().strip()
        new_password = self.profile_newpassword_lineEdit.text().strip()
        confirm_password = self.profile_confirmpassword_lineEdit.text().strip()

        # Lưu ảnh mới nếu có
        if hasattr(self, 'profile_screen') and self.profile_screen.uploaded_image_path:
            # Trong ứng dụng thực tế, đây là nơi bạn có thể lưu thông tin ảnh vào DB
            print(f"Cập nhật ảnh profile: {self.profile_screen.uploaded_image_path}")
            # TODO: Thêm code lưu ảnh vào DB

        update_result, message = self.profile.update_profile(old_username, new_username, new_fullname, current_password, new_password, confirm_password)

        if update_result:
            QtWidgets.QMessageBox.information(self.body_stackedWidget, "Success", "User update successful!")
            self.profile_currentpassword_lineEdit.clear()
            self.profile_newpassword_lineEdit.clear()
            self.profile_confirmpassword_lineEdit.clear()
        else:
            QtWidgets.QMessageBox.warning(self.body_stackedWidget, "Error", message)

    def logout(self):
        self.menu_dock.setVisible(False)
        confirmation = QMessageBox()
        confirmation.setIcon(QMessageBox.Icon.Question)
        confirmation.setWindowTitle("Logout Confirmation")
        confirmation.setText("Are you sure you want to log out?")
        confirmation.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirmation.setDefaultButton(QMessageBox.StandardButton.No)

        if confirmation.exec() == QMessageBox.StandardButton.Yes:
            if self.db_manager.logout_user(self.username):
                print("Logout successful! Returning to login screen...")
                self.stackedWidget.setCurrentWidget(self.Login_SignUp)
                self.goLogin()
                self.profile = None
                self.fullname = None
            else:
                print("Logout failed!")

    def goLogin(self):
        self.login_signup_stackedWidget.setCurrentWidget(self.right_login_page)

    def goSignUp(self):
        self.login_signup_stackedWidget.setCurrentWidget(self.right_signup_page)

    def goHome(self):
        self.menu_dock.setVisible(False)
        self.body_stackedWidget.setCurrentWidget(self.home_page)

    def goRestaurant(self):
        self.menu_dock.setVisible(False)
        # if not hasattr(self.body_stackedWidget, "restaurant_page") or self.body_stackedWidget.restaurant_page is None:
        #     self.setup_restaurant()
        self.setup_restaurant()

        self.body_stackedWidget.setCurrentWidget(self.restaurant_page)
        # self.restaurant_stackedWidget.setCurrentWidget(self.restaurant_page)
        self.restaurant_page.setVisible(True)
        print(f"restaurant_page visibility after setting: {self.restaurant_page.isVisible()}")

    def setup_restaurant(self):
        self.restaurant_page = RestaurantScreen(parent=self)
        self.restaurant_page_layout = QVBoxLayout(self.restaurant_page)
        self.restaurant_page_layout.setContentsMargins(0, 0, 0, 0)
        self.body_stackedWidget.addWidget(self.restaurant_page)

    def setup_menuburger(self):
        self.menu_dock = QDockWidget(self.centralwidget)
        self.menu_dock.setAllowedAreas(Qt.DockWidgetArea.NoDockWidgetArea)
        self.menu_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.menu_dock.setVisible(False)

        title_bar = QtWidgets.QWidget()
        title_bar.setFixedHeight(50)
        title_layout = QVBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)

        menu_button = QPushButton("☰ Menu", title_bar)
        menu_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #696D5E;
                color: white;
                padding: 10px;
                text-align: left;
                border: none;
            }
            QPushButton:hover {
                background-color: #5A5E50;
            }
        """)
        menu_button.setFixedHeight(50)
        menu_button.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_button.clicked.connect(self.toggle_menu)

        title_layout.addWidget(menu_button)
        self.menu_dock.setTitleBarWidget(title_bar)

        self.menu_frame = QFrame()
        self.menu_frame.setStyleSheet("""
            background-color: #A6A690;
            border-radius-bottom-left: 20px;
            border-radius-bottom-right:20px;
        """)
        self.menu_frame.setFixedWidth(180)

        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)

        self.menu_list = QListWidget(self.menu_frame)
        self.menu_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
            }
            QListWidget::item {
                font-size: 20px;
                padding: 10px;
                background-color: #C1C6B9;
                border-bottom: 1px solid #33372C;
            }
            QListWidget::item:hover {
                background-color: #C5C5A5;
            }
        """)
        self.menu_list.setMouseTracking(True)

        menu_items = [("Profile", self.goProfile),
                      ("Restaurants", self.goRestaurant),
                      ("Menu Items", self.goMenu),
                      ("Log out", self.logout)]

        for index, (name, function) in enumerate(menu_items):
            item = QListWidgetItem(name)
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.menu_list.addItem(item)

        self.menu_list.setFixedHeight(len(menu_items) * 40)
        self.menu_list.itemClicked.connect(lambda item: self.handle_menu_click(item, menu_items))
        self.menu_list.enterEvent = lambda event: self.menu_list.setCursor(Qt.CursorShape.PointingHandCursor)
        self.menu_list.leaveEvent = lambda event: self.menu_list.setCursor(Qt.CursorShape.ArrowCursor)

        menu_layout.addWidget(self.menu_list)
        self.menu_frame.setLayout(menu_layout)
        self.menu_dock.setWidget(self.menu_frame)
        # Position the menu at the right side
        self.menu_dock.move(self.width - self.menu_frame.width(), self.header_frame.height())

    def goMenu(self):
        self.menu_dock.setVisible(False)
        self.body_stackedWidget.setCurrentWidget(self.inside_restaurant_page)
        if not hasattr(self.body_stackedWidget, "all_menu_page") or self.body_stackedWidget.all_menu_page is None:
            self.body_stackedWidget.all_menu_page = AllMenuItemScreen(parent=self)
            self.body_stackedWidget.addWidget(self.body_stackedWidget.all_menu_page)
        self.body_stackedWidget.setCurrentWidget(self.body_stackedWidget.all_menu_page)
        self.body_stackedWidget.all_menu_page.setVisible(True)
        self.body_stackedWidget.all_menu_page.tableWidget.setVisible(True)
        self.body_stackedWidget.all_menu_page.update()
        self.body_stackedWidget.all_menu_page.repaint()
        print(f"all_menu_page visibility after setting: {self.body_stackedWidget.all_menu_page.isVisible()}")
        print(f"all_menu_page tableWidget visibility: {self.body_stackedWidget.all_menu_page.tableWidget.isVisible()}")

    def handle_menu_click(self, item, menu_items):
        for name, function in menu_items:
            if item.text() == name:
                function()

    def toggle_menu(self):
        if self.menu_dock.isVisible():
            self.menu_dock.setVisible(False)
        else:
            self.menu_dock.setVisible(True)

    def update_menu_position(self):
        button_x = self.burger_menu_button.mapToGlobal(self.burger_menu_button.rect().topLeft()).x()
        button_y = self.burger_menu_button.mapToGlobal(self.burger_menu_button.rect().bottomLeft()).y()
        self.menu_dock.setGeometry(button_x, button_y, 150, 200)

    def goProfile(self):
        self.menu_dock.setVisible(False)
        self.fullname = self.profile.current_user.fullname
        self.profile_fullname_lineEdit.setText(self.fullname)
        self.body_stackedWidget.setCurrentWidget(self.profile_page)
        self.profile_username_lineEdit.setText(self.username)
        
        # Clear password fields when navigating to profile page
        self.profile_currentpassword_lineEdit.clear()
        self.profile_newpassword_lineEdit.clear()
        self.profile_confirmpassword_lineEdit.clear()
        
        # Khởi tạo ProfileScreen nếu chưa tồn tại
        if not hasattr(self, 'profile_screen'):
            self.profile_screen = ProfileScreen(parent=self)
        
        # Load lại hình ảnh profile nếu cần
        self.profile_screen.load_default_images()
        
        # Nếu trong tương lai có ảnh đã lưu trong DB cho user này
        # image_url = self.profile.current_user.profile_image_url
        # if image_url:
        #     self.profile_screen.update_profile_photo(image_url)

    def login(self):
        self.username = self.login_username_lineEdit.text().strip()
        password = self.login_password_lineEdit.text()

        success = self.db_manager.login_user(self.username, password)

        if success:
            QtWidgets.QMessageBox.information(self.login_signup_stackedWidget, "Success", "Login successful!")
            print("setting up profile page")
            self.stackedWidget.setCurrentWidget(self.Main)
            self.profile = ProfileModel(self.db_manager, self.username)
            
            # Khởi tạo ProfileScreen sau khi đăng nhập
            if not hasattr(self, 'profile_screen'):
                self.profile_screen = ProfileScreen(parent=self)
                
            self.goProfile()
            self.login_password_lineEdit.clear()
            self.login_username_lineEdit.clear()
        else:
            QtWidgets.QMessageBox.warning(self.login_signup_stackedWidget, "Error", "Invalid username or password!")

    def signup(self):
        self.username = self.signup_username_lineEdit.text().strip()
        self.fullname = self.signup_fullname_lineEdit.text().strip()
        password = self.signup_password_lineEdit.text()
        confirm_password = self.signup_confirmpass_lineEdit.text()

        db_manager = DatabaseManager()
        if self.username == "" or self.fullname == "" or password == "" or confirm_password == "":
            QtWidgets.QMessageBox.warning(self.welcome_stackedWidget, "Error", "All fields are required!")
        elif password == confirm_password:
            success = db_manager.register_user(self.username, self.fullname, password)

            if success:
                QtWidgets.QMessageBox.information(self.welcome_stackedWidget, "Success", "User registered successfully!")
                print("setting up profile page")
                self.profile = ProfileModel(self.db_manager, self.username)
                
                # Khởi tạo ProfileScreen sau khi đăng ký
                if not hasattr(self, 'profile_screen'):
                    self.profile_screen = ProfileScreen(parent=self)
                    
                self.stackedWidget.setCurrentWidget(self.Main)
                self.goProfile()
                self.signup_password_lineEdit.clear()
                self.signup_confirmpass_lineEdit.clear()
                self.signup_fullname_lineEdit.clear()
                self.signup_username_lineEdit.clear()
            else:
                QtWidgets.QMessageBox.warning(self.welcome_stackedWidget, "Error", "Username or email already exists!")
        else:
            QtWidgets.QMessageBox.warning(self.welcome_stackedWidget, "Error", "Password and confirm password do not match!")

    def removeAllWidgetsExcept(self, stack: QtWidgets.QStackedWidget, w: QtWidgets.QWidget):
        for i in reversed(range(stack.count())):
            widget = stack.widget(i)
            if widget is not w:
                print('removed', widget.objectName())
                stack.removeWidget(widget)
                widget.deleteLater()

    def show_menu_for_restaurant(self, place_id):
        print(f"Extend_MainWindow: Showing menu for place_id: {place_id}")
        self.body_stackedWidget.setCurrentWidget(self.inside_restaurant_page)

        # Xóa menu_page cũ nếu tồn tại
        if hasattr(self.body_stackedWidget, 'menu_page') and self.body_stackedWidget.menu_page is not None:
            print("Removing existing menu_page")
            self.restaurant_stackedWidget.removeWidget(self.body_stackedWidget.menu_page)
            self.body_stackedWidget.menu_page.deleteLater()
            delattr(self.body_stackedWidget, 'menu_page')

        # Tạo menu_page mới
        self.body_stackedWidget.menu_page = RestaurantMenuScreen(place_id=place_id, parent=self)
        self.restaurant_stackedWidget.addWidget(self.body_stackedWidget.menu_page)

        # Đặt menu_page làm widget hiện tại
        self.restaurant_stackedWidget.setCurrentWidget(self.body_stackedWidget.menu_page)
        self.body_stackedWidget.menu_page.setVisible(True)
        self.restaurant_stackedWidget.setVisible(True)
        self.body_stackedWidget.setVisible(True)

        # Đảm bảo tableWidget hiển thị
        self.body_stackedWidget.menu_page.tableWidget.setVisible(True)

        # Gọi update và repaint để đảm bảo giao diện được vẽ lại
        self.body_stackedWidget.menu_page.update()
        self.body_stackedWidget.menu_page.repaint()
        self.body_stackedWidget.menu_page.tableWidget.update()
        self.body_stackedWidget.menu_page.tableWidget.repaint()

        # Log trạng thái
        print(f"menu_page visibility after setting: {self.body_stackedWidget.menu_page.isVisible()}")
        print(f"tableWidget visibility after setting: {self.body_stackedWidget.menu_page.tableWidget.isVisible()}")
        print(f"restaurant_stackedWidget visible: {self.restaurant_stackedWidget.isVisible()}")
        print(f"body_stackedWidget visible: {self.body_stackedWidget.isVisible()}")

    def show_all_menu_items(self):
        """Hiển thị tất cả menu items"""
        print("Extend_MainWindow: show_all_menu_items called")
        self.menu_dock.setVisible(False)
        self.body_stackedWidget.setCurrentWidget(self.inside_restaurant_page)

        # Kiểm tra nếu all_menu_page chưa được tạo
        if not hasattr(self.body_stackedWidget, "all_menu_page") or self.body_stackedWidget.all_menu_page is None:
            print("all_menu_page chưa tồn tại. Đang tạo mới...")
            self.body_stackedWidget.all_menu_page = AllMenuItemScreen(parent=self)
            self.restaurant_stackedWidget.addWidget(self.body_stackedWidget.all_menu_page)
        else:
            print("all_menu_page đã tồn tại. Tải lại dữ liệu...")
            self.body_stackedWidget.all_menu_page.load_menu_data()

        # Đặt all_menu_page làm widget hiện tại
        self.restaurant_stackedWidget.setCurrentWidget(self.body_stackedWidget.all_menu_page)

        # Đảm bảo all_menu_page hiển thị
        self.body_stackedWidget.all_menu_page.setVisible(True)
        self.body_stackedWidget.all_menu_page.tableWidget.setVisible(True)

        # Gọi update và repaint để đảm bảo giao diện được vẽ lại
        self.body_stackedWidget.all_menu_page.update()
        self.body_stackedWidget.all_menu_page.repaint()
        self.body_stackedWidget.all_menu_page.tableWidget.update()
        self.body_stackedWidget.all_menu_page.tableWidget.repaint()

        # Log trạng thái
        print(f"all_menu_page visibility after setting: {self.body_stackedWidget.all_menu_page.isVisible()}")
        print(f"tableWidget visibility after setting: {self.body_stackedWidget.all_menu_page.tableWidget.isVisible()}")

    def setup_pages(self):
        # Tạo inside_restaurant_page
        self.inside_restaurant_page = QWidget()
        self.inside_restaurant_page_layout = QVBoxLayout(self.inside_restaurant_page)
        self.inside_restaurant_page_layout.setContentsMargins(0, 0, 0, 0)

        # Tạo restaurant_stackedWidget
        self.restaurant_stackedWidget = QtWidgets.QStackedWidget()
        self.inside_restaurant_page_layout.addWidget(self.restaurant_stackedWidget)

        # Thêm inside_restaurant_page vào body_stackedWidget
        self.body_stackedWidget.addWidget(self.inside_restaurant_page)

        # Khởi tạo restaurant_page
        self.restaurant_page = RestaurantScreen(parent=self)
        self.restaurant_stackedWidget.addWidget(self.restaurant_page)

        # Không khởi tạo menu_page và all_menu_page tại đây
        # Chúng sẽ được tạo khi cần trong show_menu_for_restaurant và show_all_menu_items

        print("setup_pages completed")