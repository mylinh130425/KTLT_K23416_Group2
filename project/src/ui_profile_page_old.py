# Form implementation generated from reading ui file 'D:\Document\Bachelor\UEL\ProgrammingTechniquesKTLT\KTLT-group2\project\generated-files/ui/new_profile_page.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(725, 382)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.left_panel_profile = QtWidgets.QVBoxLayout()
        self.left_panel_profile.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.left_panel_profile.setObjectName("left_panel_profile")
        self.pushButton_5 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_5.setObjectName("pushButton_5")
        self.left_panel_profile.addWidget(self.pushButton_5)
        self.horizontalLayout.addLayout(self.left_panel_profile)
        self.frame_5 = QtWidgets.QFrame(parent=Form)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_24.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.signup_photo_label_2 = QtWidgets.QLabel(parent=self.frame_5)
        self.signup_photo_label_2.setMinimumSize(QtCore.QSize(90, 90))
        self.signup_photo_label_2.setMaximumSize(QtCore.QSize(90, 90))
        self.signup_photo_label_2.setStyleSheet("border-radius: 45px;  border: 1.5px solid #333;")
        self.signup_photo_label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.signup_photo_label_2.setObjectName("signup_photo_label_2")
        self.verticalLayout_24.addWidget(self.signup_photo_label_2, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_25 = QtWidgets.QVBoxLayout()
        self.verticalLayout_25.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_25.setContentsMargins(50, 0, 50, 0)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout()
        self.verticalLayout_26.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_26.setContentsMargins(-1, 0, 0, 15)
        self.verticalLayout_26.setSpacing(6)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.full_name_lineEdit_2 = QtWidgets.QLineEdit(parent=self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.full_name_lineEdit_2.sizePolicy().hasHeightForWidth())
        self.full_name_lineEdit_2.setSizePolicy(sizePolicy)
        self.full_name_lineEdit_2.setMinimumSize(QtCore.QSize(0, 25))
        self.full_name_lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 25))
        self.full_name_lineEdit_2.setStyleSheet("")
        self.full_name_lineEdit_2.setText("")
        self.full_name_lineEdit_2.setObjectName("full_name_lineEdit_2")
        self.verticalLayout_26.addWidget(self.full_name_lineEdit_2)
        self.signup_username_lineEdit_2 = QtWidgets.QLineEdit(parent=self.frame_5)
        self.signup_username_lineEdit_2.setMinimumSize(QtCore.QSize(0, 25))
        self.signup_username_lineEdit_2.setStyleSheet("")
        self.signup_username_lineEdit_2.setObjectName("signup_username_lineEdit_2")
        self.verticalLayout_26.addWidget(self.signup_username_lineEdit_2)
        self.signup_password_lineEdit_2 = QtWidgets.QLineEdit(parent=self.frame_5)
        self.signup_password_lineEdit_2.setMinimumSize(QtCore.QSize(0, 25))
        self.signup_password_lineEdit_2.setStyleSheet("")
        self.signup_password_lineEdit_2.setObjectName("signup_password_lineEdit_2")
        self.verticalLayout_26.addWidget(self.signup_password_lineEdit_2)
        self.verticalLayout_25.addLayout(self.verticalLayout_26)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout_4.setContentsMargins(-1, 15, -1, 0)
        self.horizontalLayout_4.setSpacing(50)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.to_login_button_2 = QtWidgets.QPushButton(parent=self.frame_5)
        self.to_login_button_2.setMinimumSize(QtCore.QSize(0, 30))
        self.to_login_button_2.setMaximumSize(QtCore.QSize(230, 30))
        self.to_login_button_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.to_login_button_2.setStyleSheet("")
        self.to_login_button_2.setObjectName("to_login_button_2")
        self.horizontalLayout_4.addWidget(self.to_login_button_2)
        self.signup_button_2 = QtWidgets.QPushButton(parent=self.frame_5)
        self.signup_button_2.setMinimumSize(QtCore.QSize(0, 30))
        self.signup_button_2.setMaximumSize(QtCore.QSize(230, 30))
        self.signup_button_2.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.signup_button_2.setStyleSheet("")
        self.signup_button_2.setObjectName("signup_button_2")
        self.horizontalLayout_4.addWidget(self.signup_button_2)
        self.verticalLayout_25.addLayout(self.horizontalLayout_4)
        self.verticalLayout_24.addLayout(self.verticalLayout_25)
        self.horizontalLayout.addWidget(self.frame_5)
        self.profile_right_frame = QtWidgets.QFrame(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profile_right_frame.sizePolicy().hasHeightForWidth())
        self.profile_right_frame.setSizePolicy(sizePolicy)
        self.profile_right_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.profile_right_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.profile_right_frame.setObjectName("profile_right_frame")
        self.horizontalLayout.addWidget(self.profile_right_frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_5.setText(_translate("Form", "Logout"))
        self.signup_photo_label_2.setText(_translate("Form", "LOGO"))
        self.full_name_lineEdit_2.setPlaceholderText(_translate("Form", "Full name"))
        self.signup_username_lineEdit_2.setPlaceholderText(_translate("Form", "Email or username"))
        self.signup_password_lineEdit_2.setPlaceholderText(_translate("Form", "Password"))
        self.to_login_button_2.setText(_translate("Form", "Delete Account"))
        self.signup_button_2.setText(_translate("Form", "Save"))
