import sys

from PyQt6.QtGui import QPixmap

from src.ext_interface import *

from Custom_Widgets.Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Extend_MainWindow()
        self.ui.setupUi(self)
        loadJsonStyle(self, self.ui, jsonFiles = {
            "json-styles/login_style.json"
            })

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.show() 

        QAppSettings.updateAppSettings(self)

        self.ui.restaurant_menu_button.clicked.connect(self.show_menu_page)
        self.ui.restaurant_review_button.clicked.connect(self.show_review_page)

    def show_menu_page(self):
        self.ui.restaurant_stackedWidget.setCurrentWidget(self.ui.menu_page)

    def show_review_page(self):
        self.ui.restaurant_stackedWidget.setCurrentWidget(self.ui.review_restaurant_page)

    def changeEvent(self, event):
        """ Prevent the window from maximizing when double-clicking the title bar """
        if event.type() == event.Type.WindowStateChange:
            if self.windowState() == Qt.WindowState.WindowMaximized:
                self.showNormal()  # Restore the window to its normal size
        super().changeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = lambda exctype, value, traceback: print(exctype, value)
    sys.exit(app.exec_())
