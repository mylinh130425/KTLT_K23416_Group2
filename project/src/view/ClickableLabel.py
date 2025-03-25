from PIL.ImageQt import QPixmap
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QFileDialog


class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Custom signal for clicks

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit signal when clicked
    def open_file_dialog(self, ):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:  # If a file is selected
            self.file_path = file_path  # Save the path
            self.setPixmap(QPixmap(file_path).scaled(
                self.width(),
                self.height()
            ))  # Load image to QLabel instantly
        print(self.restaurant_new_image_path)
        return file_path