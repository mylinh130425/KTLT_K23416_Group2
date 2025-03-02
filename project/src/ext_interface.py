from PyQt6.QtWidgets import QVBoxLayout

from project.src.ext_profile_page import ProfileForm
from project.src.ui_interface import *


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
        self.profile_page2 = QtWidgets.QWidget()
        self.profile_page2.setObjectName("profile_page2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.profile_page2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.left_panel_profile = QtWidgets.QVBoxLayout()
        self.left_panel_profile.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        print("adding left panel profile")
        self.left_panel_profile.setObjectName("left_panel_profile")
        self.pushButton_213 = QtWidgets.QPushButton(parent=self.profile_page2)
        self.pushButton_213.setObjectName("pushButton_3")
        self.left_panel_profile.addWidget(self.pushButton_3)
        self.horizontalLayout_2.addLayout(self.left_panel_profile)
        self.frame_5 = QtWidgets.QFrame(parent=self.profile_page2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        print("adding frame 5")
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_16.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.signup_photo_label_2 = QtWidgets.QLabel(parent=self.frame_5)
        self.signup_photo_label_2.setMinimumSize(QtCore.QSize(90, 90))
        self.signup_photo_label_2.setMaximumSize(QtCore.QSize(90, 90))
        self.signup_photo_label_2.setStyleSheet("border-radius: 45px;  border: 1.5px solid #333;")
        self.signup_photo_label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_photo_label_2.setObjectName("signup_photo_label_2")
        self.verticalLayout_16.addWidget(self.signup_photo_label_2, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_17.setContentsMargins(50, 0, 50, 0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_18.setContentsMargins(-1, 0, 0, 15)
        self.verticalLayout_18.setSpacing(6)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.full_name_lineEdit_2 = QtWidgets.QLineEdit(parent=self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.full_name_lineEdit_2.sizePolicy().hasHeightForWidth())
        self.full_name_lineEdit_2.setSizePolicy(sizePolicy)
        self.full_name_lineEdit_2.setMinimumSize(QtCore.QSize(0, 25))
        self.full_name_lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.full_name_lineEdit_2.setStyleSheet("")
        self.full_name_lineEdit_2.setText("")
        self.full_name_lineEdit_2.setObjectName("full_name_lineEdit_2")
        self.verticalLayout_18.addWidget(self.full_name_lineEdit_2)
        self.signup_username_lineEdit_2 = QtWidgets.QLineEdit(parent=self.frame_5)
        self.signup_username_lineEdit_2.setMinimumSize(QtCore.QSize(0, 25))
        self.signup_username_lineEdit_2.setStyleSheet("")
        self.signup_username_lineEdit_2.setObjectName("signup_username_lineEdit_2")
        self.verticalLayout_18.addWidget(self.signup_username_lineEdit_2)
        self.signup_password_lineEdit_2 = QtWidgets.QLineEdit(parent=self.frame_5)
        self.signup_password_lineEdit_2.setMinimumSize(QtCore.QSize(0, 25))
        self.signup_password_lineEdit_2.setStyleSheet("")
        self.signup_password_lineEdit_2.setObjectName("signup_password_lineEdit_2")
        self.verticalLayout_18.addWidget(self.signup_password_lineEdit_2)
        self.verticalLayout_17.addLayout(self.verticalLayout_18)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout_3.setContentsMargins(-1, 15, -1, 0)
        self.horizontalLayout_3.setSpacing(50)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.to_login_button_2 = QtWidgets.QPushButton(parent=self.frame_5)
        self.to_login_button_2.setMinimumSize(QtCore.QSize(0, 30))
        self.to_login_button_2.setMaximumSize(QtCore.QSize(230, 30))
        self.to_login_button_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.to_login_button_2.setStyleSheet("")
        self.to_login_button_2.setObjectName("to_login_button_2")
        self.horizontalLayout_3.addWidget(self.to_login_button_2)
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
        self.profile_right_frame = QtWidgets.QFrame(parent=self.profile_page2)
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
        self.body_stackedWidget.addWidget(self.profile_page2)

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
        self.body_stackedWidget.setCurrentWidget(self.profile_page2)



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


