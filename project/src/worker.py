from PyQt6.QtCore import QObject, pyqtSignal, QThread
from project.src.ext_profile_page import HorizontalLayoutProfile  # Make sure this import is correct


class Worker(QObject):
    # Define signal to send the created widget to the main thread
    widgetCreated = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def createWidget(self, parentWidget):
        print("Creating widget in background...")

        # Create the widget (HorizontalLayoutProfile in this case)
        form_widget = HorizontalLayoutProfile()
        form_widget.setupUi(parentWidget)  # Set up the widget with the given parent (profile_page)

        # Emit the signal once the widget is created
        self.widgetCreated.emit(form_widget)  # Send the created widget to the main thread via widgetCreated.emit
class WorkerThread(QThread):
    def __init__(self, worker, parentWidget):
        super().__init__()
        self.worker = worker
        self.parentWidget = parentWidget

    def run(self):
        self.worker.createWidget(self.parentWidget)  # Perform the widget creation in background
