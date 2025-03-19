from project.src.ProfileScreen import ProfileScreen
from project.src.ui_interface_stacked import *


class Extend_MainWindow(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.processSignalAndSlot()

    def processSignalAndSlot(self):
        self.login_button.clicked.connect(self.loginClicked)
        self.to_login_button.clicked.connect(self.goLogin)
        self.to_signup_button.clicked.connect(self.goSignUp)
        self.home_button.clicked.connect(self.goHome)
        self.restaurant_button.clicked.connect(self.goRestaurant)

    def goLogin(self):
        self.login_signup_stackedWidget.setCurrentWidget(self.right_login_page)
    def goSignUp(self):
        self.login_signup_stackedWidget.setCurrentWidget(self.right_signup_page)

    def goHome(self):
        self.body_stackedWidget.setCurrentWidget(self.home_page)
        self.removeAllWidgetsExcept(self.body_stackedWidget,self.home_page)

    def goRestaurant(self):
        self.body_stackedWidget.setCurrentWidget(self.restaurant_page)
        self.removeAllWidgetsExcept(self.body_stackedWidget,self.restaurant_page)

    def removeAllWidgetsExcept(self, stack, w):
        for i in reversed(range(stack.count())):
            widget = stack.widget(i)
            if widget is not w:  # Chỉ xóa nếu KHÔNG phải w
                print('removed', widget.objectName())
                stack.removeWidget(widget)
                widget.deleteLater()

    def setup_profile(self):
        self.profile_page = ProfileScreen(self.body_stackedWidget)
        self.body_stackedWidget.addWidget(self.profile_page)  # Thêm trực tiếp


    def loginClicked(self):
        print("setting up profile page")
        self.setup_profile()
        self.stackedWidget.setCurrentWidget(self.Main)
        self.body_stackedWidget.setCurrentWidget(self.profile_page)


