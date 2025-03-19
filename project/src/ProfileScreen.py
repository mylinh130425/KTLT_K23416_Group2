from PyQt6 import QtCore, QtGui, QtWidgets

class ProfileScreen(QtWidgets.QWidget):  # Kế thừa từ QWidget
    def __init__(self, parent=None):
        """
        Initialize the ProfileScreen widget.

        This method will be called when an object of this class is instantiated.
        It sets up the UI of the ProfileScreen widget.
        """
        super().__init__(parent)


        self.setObjectName("profile_page")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Left panel
        self.left_panel_profile = QtWidgets.QVBoxLayout()
        self.left_panel_profile.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.left_panel_profile.setObjectName("left_panel_profile")

        self.logoutButton = QtWidgets.QPushButton(parent=self)
        self.logoutButton.setObjectName("logoutButton")
        self.left_panel_profile.addWidget(self.logoutButton)
        self.horizontalLayout_2.addLayout(self.left_panel_profile)

        # Profile frame
        self.frame_5 = QtWidgets.QFrame(parent=self)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
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
        self.profile_photo_label.setObjectName("profile_photo_label")
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


        # Right panel
        self.profile_right_frame = QtWidgets.QFrame(parent=self)
        self.profile_right_frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                                                    QtWidgets.QSizePolicy.Policy.Expanding))
        self.profile_right_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.profile_right_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.profile_right_frame.setObjectName("profile_right_frame")
        self.horizontalLayout_2.addWidget(self.profile_right_frame)
