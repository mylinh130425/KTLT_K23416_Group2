#########################################################################
## IMPORTS
########################################################################
import os
import sys

from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QLayout

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
########################################################################
class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Extend_MainWindow()
        self.ui.setupUi(self)

        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        #Use this if you only have one json file named "login_style.json" inside the root directory, "json" directory or "jsonstyles" folder.
        # loadJsonStyle(self, self.ui) 

        # Use this to specify your json file(s) path/name
        loadJsonStyle(self, self.ui, jsonFiles = {
            "json-styles/login_style.json"
            })

        #code for preventing resize
        # self.setWindowFlags(Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)



        ########################################################################

        #######################################################################
        # SHOW WINDOW
        #######################################################################
        self.show() 

        ########################################################################
        # UPDATE APP SETTINGS LOADED FROM JSON STYLESHEET 
        # ITS IMPORTANT TO RUN THIS AFTER SHOWING THE WINDOW
        # THIS PROCESS WILL RUN ON A SEPARATE THREAD WHEN GENERATING NEW ICONS
        # TO PREVENT THE WINDOW FROM BEING UNRESPONSIVE
        ########################################################################
        # self = QMainWindow class
        QAppSettings.updateAppSettings(self)

#code for preventing resize
    # def changeEvent(self, event):
    #     """ Prevent the window from maximizing when double-clicking the title bar """
    #     if event.type() == event.Type.WindowStateChange:
    #         if self.windowState() == Qt.WindowState.WindowMaximized:
    #             self.showNormal()  # Restore the window to its normal size
    #     super().changeEvent(event)

########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ########################################################################
    ## 
    ########################################################################
    window = MainWindow()
    # window.layout().setSizeConstraint(QLayout.setFixedSize)
    window.show()
    sys.excepthook = lambda exctype, value, traceback: print(exctype, value)
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################  
