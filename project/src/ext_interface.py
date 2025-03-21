# from project.src.BurgerMenu import BurgerMenu
from project.src.DatabaseManager import DatabaseManager
from project.src.ui_profile_page import Ui_Profile
from project.src.view.RestaurantScreen import RestaurantScreen
from project.src.ui_interface_stacked import *


class Extend_MainWindow(Ui_MainWindow):
    def setupUi(self, MainWindow):
        """
        Set up the main window UI by initializing the user interface components
        and connecting signals to their respective slots.

        Args:
            MainWindow (QMainWindow): The main window to set up the UI for.
        """
        super().setupUi(MainWindow)
        # Header Bar
        # self.header_bar= HeaderBar()
        # self.header_main = None
        # Set layout for header_main and add HeaderBar inside it
        # layout = QVBoxLayout(self.header_main)
        # layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        # layout.setSpacing(0)  # Remove spacing
        # self.horizontalLayout_13.addWidget(self.header_bar, alignment=Qt.AlignmentFlag.AlignTop)

        # self.header_bar.logoClicked.connect(self.goHome)  # Connect signal to function

        self.processSignalAndSlot()
        self.db_manager = DatabaseManager()


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
        self.burger_menu_button.clicked.connect(self.goRestaurant)


        # self.burger_menu_button = BurgerMenu()
        # self.burger_menu_button.clicked.connect(self)
        # self.restaurant_button.clicked.connect(self.goRestaurant)

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
        self.body_stackedWidget.setCurrentWidget(self.home_page)
        # self.removeAllWidgetsExcept(self.body_stackedWidget,self.home_page)

    def goRestaurant(self):
        """
        Sets the restaurant page as the current widget of the
        `body_stackedWidget` and removes all other widgets except the restaurant page.
        """
        self.setup_restaurant()
        self.body_stackedWidget.setCurrentWidget(self.restaurant_page)
        # self.removeAllWidgetsExcept(self.body_stackedWidget, self.restaurant_page)

    def setup_restaurant(self):
        self.restaurant_page=RestaurantScreen(self.body_stackedWidget)
        self.body_stackedWidget.addWidget(self.restaurant_page)

    def setup_profile(self):
        """
        Initializes the profile page and adds it to the body stacked widget.

        This method creates an instance of the Ui_Profile and adds it to Ui_Profile
        `body_stackedWidget`. This allows the profile page to be displayed within
        the main application window when navigating to the profile section.
        """
        self.profile_page = Ui_Profile(self.body_stackedWidget)
        self.body_stackedWidget.addWidget(self.profile_page)  # Thêm trực tiếp


    def login(self):
        """
        Handles the login button click event.

        This method is triggered when the login button is clicked. It sets up
        the profile page, adds it to the body stacked widget, and updates the
        current widget of the stacked widget and body stacked widget to display
        the main and profile page, respectively.
        """
        # self.login_handler = LoginHandler(self)
        # isLoggedIn = self.login_handler.login()
        # if isLoggedIn:
        username = self.login_username_lineEdit.text().strip()
        password = self.login_password_lineEdit.text()

        success = self.db_manager.login_user(username, password)

        if success:
            QtWidgets.QMessageBox.information(self.login_signup_stackedWidget, "Success", "Login successful!")
            print("setting up profile page")
            self.header_frame.setStyleSheet("{background-color: #33372C}")
            self.setup_profile()
            self.stackedWidget.setCurrentWidget(self.Main)
            self.body_stackedWidget.setCurrentWidget(self.profile_page)
            # self.removeAllWidgetsExcept(self.body_stackedWidget,self.profile_page)
        else:
            QtWidgets.QMessageBox.warning(self.login_signup_stackedWidget, "Error", "Invalid username or password!")



    def signup(self):
        # self.signup_handler = SignupHandler(self)
        # isSignedup= self.signup_handler.signup()
        # if isSignedup:
        username = self.signup_username_lineEdit.text().strip()
        fullname = self.signup_fullname_lineEdit.text().strip()  # Dùng fullname field cho email
        password = self.signup_password_lineEdit.text()
        confirm_password=self.signup_confrmpass_lineEdit.text()

        db_manager = DatabaseManager()
        if username=="" or fullname=="" or password=="" or confirm_password=="":
            QtWidgets.QMessageBox.warning(self.welcome_stackedWidget, "Error", "All fields are required!")
        elif password==confirm_password:
            success = db_manager.register_user(username, fullname,password)

            if success:
                QtWidgets.QMessageBox.information(self.welcome_stackedWidget, "Success", "User registered successfully!")
                print("setting up profile page")

                self.setup_profile()
                self.stackedWidget.setCurrentWidget(self.Main)
                self.body_stackedWidget.setCurrentWidget(self.profile_page)
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

