from PyQt6.QtWidgets import QVBoxLayout

from project.src.ext_profile_page import ProfileDelegate
from project.src.ui_interface_stacked import *


class Extend_MainWindow(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.processSignalAndSlot()

    # assign signals and slots
    def processSignalAndSlot(self):
        self.login_button.clicked.connect(self.loginClicked)
        self.to_login_button.clicked.connect(self.goLogin)
        self.to_signup_button.clicked.connect(self.goSignUp)
    def goLogin(self):
        self.login_signup_stackedWidget.setCurrentWidget(self.right_login_page)
        # self.welcome_stackedWidget.setCurrentWidget(self.left_login_page)
    def goSignUp(self):
        self.login_signup_stackedWidget.setCurrentWidget(self.right_signup_page)
        # self.welcome_stackedWidget.setCurrentWidget(self.left_login_page)

    def setup_profile(self):
        print("setting up profile page")
        self.profile_page = QtWidgets.QWidget()
        self.profile_page.setObjectName("profile_page")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.profile_page)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.left_panel_profile = QtWidgets.QVBoxLayout()
        self.left_panel_profile.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        print("adding left panel profile")
        self.left_panel_profile.setObjectName("left_panel_profile")
        self.logoutButton = QtWidgets.QPushButton(parent=self.profile_page)
        self.logoutButton.setObjectName("pushButton_3")
        self.left_panel_profile.addWidget(self.pushButton_3)
        self.horizontalLayout_2.addLayout(self.left_panel_profile)
        self.frame_5 = QtWidgets.QFrame(parent=self.profile_page)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        print("adding frame 5")
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_16.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.profile_photo_label = QtWidgets.QLabel(parent=self.frame_5)
        self.profile_photo_label.setMinimumSize(QtCore.QSize(90, 90))
        self.profile_photo_label.setMaximumSize(QtCore.QSize(90, 90))
        self.profile_photo_label.setStyleSheet("border-radius: 45px;  border: 1.5px solid #333;")
        self.profile_photo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.profile_photo_label.setObjectName("signup_photo_label_2")
        self.verticalLayout_16.addWidget(self.profile_photo_label, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_17.setContentsMargins(50, 0, 50, 0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_18.setContentsMargins(-1, 0, 0, 15)
        self.verticalLayout_18.setSpacing(6)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.profile_fullname_lineEdit = QtWidgets.QLineEdit(parent=self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profile_fullname_lineEdit.sizePolicy().hasHeightForWidth())
        self.profile_fullname_lineEdit.setSizePolicy(sizePolicy)
        self.profile_fullname_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.profile_fullname_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.profile_fullname_lineEdit.setStyleSheet("")
        self.profile_fullname_lineEdit.setText("")
        self.profile_fullname_lineEdit.setObjectName("profile_fullname_lineEdit")
        self.verticalLayout_18.addWidget(self.profile_fullname_lineEdit)
        self.profile_username_lineEdit = QtWidgets.QLineEdit(parent=self.frame_5)
        self.profile_username_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.profile_username_lineEdit.setStyleSheet("")
        self.profile_username_lineEdit.setObjectName("profile_username_lineEdit")
        self.verticalLayout_18.addWidget(self.profile_username_lineEdit)
        self.profile_password_lineEdit = QtWidgets.QLineEdit(parent=self.frame_5)
        self.profile_password_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.profile_password_lineEdit.setStyleSheet("")
        self.profile_password_lineEdit.setObjectName("profile_password_lineEdit")
        self.verticalLayout_18.addWidget(self.profile_password_lineEdit)
        self.verticalLayout_17.addLayout(self.verticalLayout_18)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout_3.setContentsMargins(-1, 15, -1, 0)
        self.horizontalLayout_3.setSpacing(50)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.profile_save_button = QtWidgets.QPushButton(parent=self.frame_5)
        self.profile_save_button.setMinimumSize(QtCore.QSize(0, 30))
        self.profile_save_button.setMaximumSize(QtCore.QSize(230, 30))
        self.profile_save_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.profile_save_button.setStyleSheet("")
        self.profile_save_button.setObjectName("profile_save_button")
        self.horizontalLayout_3.addWidget(self.profile_save_button)
        self.signup_button_2 = QtWidgets.QPushButton(parent=self.frame_5)
        self.signup_button_2.setMinimumSize(QtCore.QSize(0, 30))
        self.signup_button_2.setMaximumSize(QtCore.QSize(230, 30))
        self.signup_button_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.signup_button_2.setStyleSheet("")
        self.signup_button_2.setObjectName("signup_button_2")
        self.horizontalLayout_3.addWidget(self.signup_button_2)
        self.verticalLayout_17.addLayout(self.horizontalLayout_3)
        self.verticalLayout_16.addLayout(self.verticalLayout_17)
        self.horizontalLayout_2.addWidget(self.frame_5)
        self.profile_right_frame = QtWidgets.QFrame(parent=self.profile_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profile_right_frame.sizePolicy().hasHeightForWidth())
        self.profile_right_frame.setSizePolicy(sizePolicy)
        self.profile_right_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.profile_right_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.profile_right_frame.setObjectName("profile_right_frame")
        self.horizontalLayout_2.addWidget(self.profile_right_frame)
        self.body_stackedWidget.addWidget(self.profile_page)

    # def setup_profile(self):
    #     self.profile_page = ProfileDelegate(self.body_stackedWidget)
    def loginClicked(self):
        print("setting up profile page")

        #ideally load each page from a standalone file and remove/delete the page no longer in use
        # self.profile_page2 = QtWidgets.QWidget()
        # self.profile_page2.setObjectName("profile_page2")
        # self.profile_widget = ProfileForm(parent=self.profile_page2)
        # self.profile_layout = QtWidgets.QVBoxLayout(self.profile_page2)
        # self.profile_layout.addWidget(self.profile_widget)
        # self.body_stackedWidget.addWidget(self.profile_page2)



        self.setup_profile() #ok it shows up but not ideal

        #
        # # # Setup the layout for profile_page if it doesn't have one
        # self.profile_page.layout().addLayout(form_widget)
        # # This method runs in the main thread and will be called when the widget is created
        # print("Adding widget to profile_page...")
        #
        # # Add the created widget (HorizontalLayoutProfile) to the profile_page layout
        # # self.profile_page.layout().addLayout(form_widget)

        # Switch to the profile page
        self.stackedWidget.setCurrentWidget(self.Main)
        self.body_stackedWidget.setCurrentWidget(self.profile_page)



    # def loginClicked(self):
    #     # Ensure profile_page has a layout
    #     if not self.profile_page.layout():
    #         self.profile_page.setLayout(QtWidgets.QVBoxLayout())
    #         print("setup box layout for profile")
    #     # Create the worker object
    #     worker = Worker()
    #
    #     # Connect the worker's widgetCreated signal to the main thread's method
    #     worker.widgetCreated.connect(self.addProfile)
    #
    #     # Create a thread and move the worker to that thread
    #     thread = WorkerThread(worker,self.profile_page)
    #
    #     # Start the thread (this will trigger the worker's `run()` method)
    #     thread.start()


