from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMenu
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import pyqtSignal, Qt

class HeaderBar(QWidget):
    logoClicked = pyqtSignal()  # Signal emitted when the logo is clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Create clickable logo (QLabel)
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("project/ic_food.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))  # Load your logo
        self.logo_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))  # Change cursor to pointer
        self.logo_label.mousePressEvent = self.onLogoClicked  # Assign event manually



        # Search Bar
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search Restaurant")
        self.searchBar.setFixedHeight(30)
        self.searchBar.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid gray;")

        # Menu Button
        self.menuButton = QPushButton("☰", self)
        self.menuButton.setFixedSize(40, 40)
        self.menuButton.setStyleSheet("font-size: 18px; border: none; background: none;")

        # Dropdown Menu
        self.menu = QMenu(self)
        self.menu.addAction("Profile")
        self.menu.addAction("Settings")
        self.menu.addAction("Logout")
        self.menuButton.setMenu(self.menu)

        # Add widgets to layout
        layout.addWidget(self.logo_label)
        layout.addWidget(self.searchBar, stretch=1)  # Search bar expands
        layout.addWidget(self.menuButton)

        self.setLayout(layout)

    def onLogoClicked(self, event):
        self.logoClicked.emit()  # Emit signal when logo is clicked
