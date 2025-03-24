#########################################################################
## IMPORTS
########################################################################
import os
import sys
########################################################################
# IMPORT GUI FILE
from src.ext_interface import *
########################################################################

########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
#######################################################################python -m pip install "pymongo[srv]"#

########################################################################
## MAIN WINDOW CLASS
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Extend_MainWindow()
        self.ui.setupUi(self)

        # Use this to specify your json file(s) path/name
        loadJsonStyle(self, self.ui, jsonFiles = {
            "json-styles/login_style.json"
            })
        self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
        self.show()

        # self = QMainWindow class
        QAppSettings.updateAppSettings(self)

    def changeEvent(self, event):
        """ Prevent the window from maximizing when double-clicking the title bar """
        if event.type() == event.Type.WindowStateChange:
            if self.windowState() == Qt.WindowState.WindowMaximized:
                self.showNormal()  # Restore the window to its normal size
        super().changeEvent(event)

########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ########################################################################
    ##
    ########################################################################
    window = MainWindow()
    window.show()
    sys.excepthook = lambda exctype, value, traceback: print(exctype, value)
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################
