from PyQt6.QtWidgets import QPushButton, QMenu, QAction, QWidget, QVBoxLayout


class BurgerMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Main Layout
        layout = QVBoxLayout()

        # Create a QPushButton for the burger menu
        self.burger_menu_button = QPushButton("☰ Menu", self)
        self.burger_menu_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #5D604A; /* Dark Green */
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #6F735B;
            }
        """)

        # Create the dropdown menu
        self.menu = QMenu(self)
        self.menu.setStyleSheet("""
            QMenu {
                background-color: #D4D6BC; /* Light Green */
                border-radius: 8px;
            }
            QMenu::item {
                padding: 8px 20px;
                font-size: 14px;
                color: black;
            }
            QMenu::item:selected {
                background-color: #B0B39D;
            }
        """)

        # Add menu actions
        self.profile_action = QAction("Profile", self)
        self.restaurants_action = QAction("Restaurants", self)
        self.foods_action = QAction("Foods", self)
        self.logout_action = QAction("Log out", self)

        self.menu.addAction(self.profile_action)
        self.menu.addAction(self.restaurants_action)
        self.menu.addAction(self.foods_action)
        self.menu.addAction(self.logout_action)

        # Connect button to open menu
        self.burger_menu_button.setMenu(self.menu)

        # Add to layout
        layout.addWidget(self.burger_menu_button)
        self.setLayout(layout)
