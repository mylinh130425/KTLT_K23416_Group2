# from project.src.BurgerMenu import BurgerMenu
from PyQt6.QtWidgets import QMessageBox, QFrame, QVBoxLayout, QPushButton, QDockWidget, QMainWindow, QListWidgetItem, \
    QListWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor
from project.src.DatabaseManager import DatabaseManager
from project.src.model.ProfileModel import ProfileModel
from project.src.ui_profile_page import Ui_Profile
from project.src.view.RestaurantScreen import RestaurantScreen
from project.src.ui_interface_stacked import *


class Extend_MainWindow(QMainWindow, Ui_MainWindow):
    def setupUi(self, MainWindow):
        """
        Set up the main window UI by initializing the user interface components
        and connecting signals to their respective slots.

        Args:
            MainWindow (QMainWindow): The main window to set up the UI for.
        """
        super().setupUi(MainWindow)
        self.width = MainWindow.width()
        self.height = MainWindow.height()
        self.processSignalAndSlot()
        self.db_manager = DatabaseManager()
        self.username=None
        self.fullname =None
        self.profile = None
        self.stackedWidget.setCurrentWidget(self.Login_SignUp)
        self.login_signup_stackedWidget.setCurrentWidget(self.right_login_page)
        self.setup_menuburger()


    def processSignalAndSlot(self):
        """
        Connects UI buttons to their respective slot functions to handle user interactions.

        This method establishes connections between the click events of the main
        navigation buttons and their corresponding slot methods. Each button, when
        clicked, triggers its associated function to navigate within the application
        or perform specific actions.
        """
        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.signup)
        self.to_login_button.clicked.connect(self.goLogin)
        self.to_signup_button.clicked.connect(self.goSignUp)
        self.home_button.clicked.connect(self.goHome)
        # self.burger_menu_button.clicked.connect(self.goRestaurant)
        self.profile_logout_button.clicked.connect(self.logout)
        self.profile_save_button.clicked.connect(self.updateProfile)
        self.profile_delete_button.clicked.connect(self.deleteProfile)
        self.burger_menu_button.clicked.connect(self.toggle_menu)
        self.centralwidget.installEventFilter(self)


        # self.burger_menu_button = BurgerMenu()
        # self.burger_menu_button.clicked.connect(self)
        # self.restaurant_button.clicked.connect(self.goRestaurant)

    def eventFilter(self, obj, event):
        """ Detect clicks outside the menu_dock and close it """
        if event.type() == event.Type.MouseButtonPress:
            if self.menu_dock.isVisible():
                # Check if the click is outside menu_dock
                if not self.menu_dock.geometry().contains(event.globalPosition().toPoint()):
                    self.menu_dock.setVisible(False)  # Hide the menu
                    return True  # Event handled

        return super().eventFilter(obj, event)  # Pass other events normally

    def deleteProfile(self):
        """Confirm and delete user profile"""
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
                self.username=None
            else:
                QMessageBox.critical(self.body_stackedWidget, "Error", "Failed to delete your profile. Please try again.")

    def updateProfile(self):
        old_username= self.username
        new_username = self.profile_username_lineEdit.text().strip()
        new_fullname = self.profile_fullname_lineEdit.text().strip()
        current_password = self.profile_currentpassword_lineEdit.text().strip()
        new_password = self.profile_newpassword_lineEdit.text().strip()
        confirm_password = self.profile_confirmpassword_lineEdit.text().strip()

        update_result,message = self.profile.update_profile(old_username, new_username, new_fullname, current_password, new_password, confirm_password)

        if update_result:
            QtWidgets.QMessageBox.information(self.body_stackedWidget, "Success", "User update successful!")
            self.profile_currentpassword_lineEdit.clear()
            self.profile_newpassword_lineEdit.clear()
            self.profile_confirmpassword_lineEdit.clear()


    def logout(self):
        self.menu_dock.setVisible(False)
        # Create a confirmation dialog
        confirmation = QMessageBox()
        confirmation.setIcon(QMessageBox.Icon.Question)
        confirmation.setWindowTitle("Logout Confirmation")
        confirmation.setText("Are you sure you want to log out?")
        confirmation.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirmation.setDefaultButton(QMessageBox.StandardButton.No)

        # If user confirms, proceed with logout
        if confirmation.exec() == QMessageBox.StandardButton.Yes:
            if self.db_manager.logout_user(self.username):

                print("✅ Logout successful! Returning to login screen...")
                # Logic để quay lại màn hình đăng nhập, ví dụ:
                self.stackedWidget.setCurrentWidget(self.Login_SignUp)
                self.goLogin()
                self.profile = None
                self.fullname=None
            else:
                print("❌ Logout failed!")

    def goLogin(self):
        """
        Sets the login page as the current widget of the
        `login_signup_stackedWidget`.
        """
        self.login_signup_stackedWidget.setCurrentWidget(self.right_login_page)


    def goSignUp(self):
        """
        Sets the signup page as the current widget of the
        `login_signup_stackedWidget`.
        """
        self.login_signup_stackedWidget.setCurrentWidget(self.right_signup_page)

    def goHome(self):
        """
        Sets the home page as the current widget of the
        `body_stackedWidget` and removes all other widgets except the home page.
        """
        self.menu_dock.setVisible(False)

        self.body_stackedWidget.setCurrentWidget(self.home_page)
        # self.removeAllWidgetsExcept(self.body_stackedWidget,self.home_page)

    def goRestaurant(self):
        """
        Sets the restaurant page as the current widget of the
        `body_stackedWidget` and removes all other widgets except the restaurant page.
        """
        self.menu_dock.setVisible(False)

        self.setup_restaurant()
        self.body_stackedWidget.setCurrentWidget(self.restaurant_page)
        # self.removeAllWidgetsExcept(self.body_stackedWidget, self.restaurant_page)

    def setup_restaurant(self):
        self.restaurant_page=RestaurantScreen(self)
        self.body_stackedWidget.addWidget(self.restaurant_page)

    def setup_menuburger(self):
        """Creates a dropdown menu using QDockWidget with QListWidget."""

        self.menu_dock = QDockWidget(self.centralwidget)
        self.menu_dock.setAllowedAreas(Qt.DockWidgetArea.NoDockWidgetArea)
        self.menu_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)  # Disable dragging
        # self.menu_dock.setTitleBarWidget(QFrame())  # Hide title bar
        self.menu_dock.setVisible(False)  # Start hidden
        # Create custom title bar
        title_bar = QtWidgets.QWidget()
        title_bar.setFixedHeight(50)
        title_layout = QVBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Create "☰ Menu" button in the title bar
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
        self.menu_dock.setTitleBarWidget(title_bar)  # Set custom title bar

        # Create menu frame
        self.menu_frame = QFrame()
        self.menu_frame.setStyleSheet("""
            background-color: #A6A690;
            border-radius-bottom-left: 20px;
            border-radius-bottom-right:20px;
        """)
        self.menu_frame.setFixedWidth(180)

        # Layout for the frame
        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)

        # Create a QListWidget for menu items
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
        self.menu_list.setMouseTracking(True)  # Enable tracking for cursor change

        # Menu items and functions
        menu_items = [ ("Profile", self.goProfile),
                      ("Restaurants", self.goRestaurant),
                      ("Menu Items", self.goRestaurant),
                      ("Log out", self.logout)]

        # Add items to QListWidget
        for index, (name, function) in enumerate(menu_items):
            item = QListWidgetItem(name)


            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.menu_list.addItem(item)

        # Set the total height for QListWidget to fit all items
        self.menu_list.setFixedHeight(len(menu_items)*40)

        # Connect click event
        self.menu_list.itemClicked.connect(lambda item: self.handle_menu_click(item, menu_items))
        # Override mouse move event to change cursor when hovering over items
        self.menu_list.enterEvent = lambda event: self.menu_list.setCursor(Qt.CursorShape.PointingHandCursor)
        self.menu_list.leaveEvent = lambda event: self.menu_list.setCursor(Qt.CursorShape.ArrowCursor)

        # Add menu_list to layout
        menu_layout.addWidget(self.menu_list)
        self.menu_frame.setLayout(menu_layout)
        self.menu_dock.setWidget(self.menu_frame)
        # Position the menu at the right side
        self.menu_dock.move(self.width - self.menu_frame.width(),
                            # self.burger_menu_button.height() +
                            self.header_frame.height())

    def handle_menu_click(self, item, menu_items):
        """Handles menu item clicks."""
        for name, function in menu_items:
            if item.text() == name:
                function()

    def toggle_menu(self):
        """ Hiển thị hoặc ẩn menu dropdown """
        if self.menu_dock.isVisible():
            self.menu_dock.setVisible(False)
        else:

            self.menu_dock.setVisible(True)


    def update_menu_position(self):
        """ Định vị menu ngay dưới burger button """
        button_x = self.burger_menu_button.mapToGlobal(self.burger_menu_button.rect().topLeft()).x()
        button_y = self.burger_menu_button.mapToGlobal(self.burger_menu_button.rect().bottomLeft()).y()
        self.menu_dock.setGeometry(button_x, button_y, 150, 200)

    def resizeEvent(self, event):
        """ Cập nhật vị trí menu khi cửa sổ thay đổi kích thước """
        self.burger_menu_button.move(self.centralwidget.width() - 50, 5)
        if self.menu_dock.isVisible():
            self.update_menu_position()
        super().resizeEvent(event)


    # def setup_profile(self):
    #     self.profile_page = Ui_Profile(self.body_stackedWidget)
    #     self.body_stackedWidget.addWidget(self.profile_page)  # Thêm trực tiếp

    def goProfile(self):
        self.menu_dock.setVisible(False)
        self.fullname = self.profile.current_user.fullname

        self.profile_fullname_lineEdit.setText(self.fullname)
        self.body_stackedWidget.setCurrentWidget(self.profile_page)
        self.profile_username_lineEdit.setText(self.username)


    def login(self):
        """
        Handles the login button click event.

        This method is triggered when the login button is clicked. It sets up
        the profile page, adds it to the body stacked widget, and updates the
        current widget of the stacked widget and body stacked widget to display
        the main and profile page, respectively.
        """
        self.username = self.login_username_lineEdit.text().strip()
        password = self.login_password_lineEdit.text()

        success = self.db_manager.login_user(self.username, password)

        if success:
            QtWidgets.QMessageBox.information(self.login_signup_stackedWidget, "Success", "Login successful!")
            print("setting up profile page")
            # self.header_frame.setStyleSheet("{background-color: #33372C}")
            # self.setup_profile()
            self.stackedWidget.setCurrentWidget(self.Main)
            self.profile = ProfileModel(self.db_manager, self.username)
            self.goProfile()
            # self.removeAllWidgetsExcept(self.body_stackedWidget,self.profile_page)
            self.login_password_lineEdit.clear()
            self.login_username_lineEdit.clear()
        else:
            QtWidgets.QMessageBox.warning(self.login_signup_stackedWidget, "Error", "Invalid username or password!")



    def signup(self):
        # self.signup_handler = SignupHandler(self)
        # isSignedup= self.signup_handler.signup()
        # if isSignedup:
        self.username = self.signup_username_lineEdit.text().strip()
        self.fullname = self.signup_fullname_lineEdit.text().strip()  # Dùng fullname field cho email
        password = self.signup_password_lineEdit.text()
        confirm_password=self.signup_confirmpass_lineEdit.text()

        db_manager = DatabaseManager()
        if self.username=="" or self.fullname=="" or password=="" or confirm_password=="":
            QtWidgets.QMessageBox.warning(self.welcome_stackedWidget, "Error", "All fields are required!")
        elif password==confirm_password:
            success = db_manager.register_user(self.username, self.fullname,password)

            if success:
                QtWidgets.QMessageBox.information(self.welcome_stackedWidget, "Success", "User registered successfully!")
                print("setting up profile page")

                # self.setup_profile()
                self.profile = ProfileModel(self.db_manager, self.username)
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
        """
        Removes all widgets from the given stack except the one specified.

        This method goes through all the widgets in the stack and removes each one
        that is not the widget specified by the `w` argument. This is done by
        iterating over the widgets in reverse order, calling `removeWidget` and
        `deleteLater` on each one.

        Args:
            stack (QtWidgets.QStackedWidget): The stack to remove widgets from.
            w (QtWidgets.QWidget): The only widget to keep in the stack.
        """
        for i in reversed(range(stack.count())):
            widget = stack.widget(i)
            if widget is not w:  # Chỉ xóa nếu KHÔNG phải w
                print('removed', widget.objectName())
                stack.removeWidget(widget)
                widget.deleteLater()

