# Form implementation generated from reading ui file 'D:\Document\Bachelor\UEL\ProgrammingTechniquesKTLT\KTLT-group2\project\generated-files/ui/new_menu_page.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(788, 514)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=Form)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.menu_page = QtWidgets.QWidget()
        self.menu_page.setObjectName("menu_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.menu_page)
        self.verticalLayout.setObjectName("verticalLayout")
        self.menu_verticalLayout = QtWidgets.QVBoxLayout()
        self.menu_verticalLayout.setObjectName("menu_verticalLayout")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.horizontalLayout_22.setSpacing(5)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.menu_page)
        self.pushButton_4.setStyleSheet("")
        self.pushButton_4.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:\\Document\\Bachelor\\UEL\\ProgrammingTechniquesKTLT\\KTLT-group2\\project\\generated-files/ui\\../image/ic_filter24.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_4.setIcon(icon)
        self.pushButton_4.setIconSize(QtCore.QSize(30, 20))
        self.pushButton_4.setShortcut("")
        self.pushButton_4.setAutoDefault(False)
        self.pushButton_4.setDefault(False)
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_22.addWidget(self.pushButton_4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem)
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.menu_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setMinimumSize(QtCore.QSize(70, 25))
        self.pushButton_8.setMaximumSize(QtCore.QSize(70, 25))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setStyleSheet("color: #FABC3F;background-color: #343131;")
        self.pushButton_8.setDefault(True)
        self.pushButton_8.setFlat(False)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_22.addWidget(self.pushButton_8)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.menu_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QtCore.QSize(70, 25))
        self.pushButton_3.setMaximumSize(QtCore.QSize(70, 25))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("color: #FABC3F;background-color: #343131;")
        self.pushButton_3.setDefault(True)
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_22.addWidget(self.pushButton_3)
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.menu_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setMinimumSize(QtCore.QSize(70, 25))
        self.pushButton_9.setMaximumSize(QtCore.QSize(70, 25))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setStyleSheet("color: #FABC3F;background-color: #343131;")
        self.pushButton_9.setDefault(True)
        self.pushButton_9.setFlat(False)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_22.addWidget(self.pushButton_9)
        self.menu_verticalLayout.addLayout(self.horizontalLayout_22)
        self.tableWidget = QtWidgets.QTableWidget(parent=self.menu_page)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(750, 400))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 167772))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("\n"
"background-color: rgb(255, 243, 228);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(52, 49, 49))
        brush = QtGui.QBrush(QtGui.QColor(250, 188, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(52, 49, 49))
        brush = QtGui.QBrush(QtGui.QColor(250, 188, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(52, 49, 49))
        brush = QtGui.QBrush(QtGui.QColor(250, 188, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(52, 49, 49))
        brush = QtGui.QBrush(QtGui.QColor(250, 188, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(52, 49, 49))
        brush = QtGui.QBrush(QtGui.QColor(250, 188, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        item.setForeground(brush)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(30)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.menu_verticalLayout.addWidget(self.tableWidget)
        self.verticalLayout.addLayout(self.menu_verticalLayout)
        self.stackedWidget.addWidget(self.menu_page)
        self.verticalLayout_2.addWidget(self.stackedWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_8.setToolTip(_translate("Form", "<html><head/><body><p><br/></p></body></html>"))
        self.pushButton_8.setText(_translate("Form", "Add"))
        self.pushButton_3.setToolTip(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Edit</span></p></body></html>"))
        self.pushButton_3.setText(_translate("Form", "Edit"))
        self.pushButton_9.setToolTip(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Edit</span></p></body></html>"))
        self.pushButton_9.setText(_translate("Form", "Delete"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "FOOD"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "RATE"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "PRICE"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "DESCRIPTION"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "REVIEW"))
