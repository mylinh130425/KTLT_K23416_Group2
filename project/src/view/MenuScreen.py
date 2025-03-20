from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from project.src.delegate.MenuDelegate import MenuDelegate

class MenuScreen(QWidget):
    def __init__(self, place_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Menu")

        layout = QVBoxLayout(self)
        self.menu_table = MenuDelegate(place_id)
        layout.addWidget(self.menu_table)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.close)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
