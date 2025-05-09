from PyQt5.QtWidgets import QStatusBar

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #333; color: #FFF;")
        self.showMessage("Ready")  # Initial message

    def update_status(self, message):
        self.showMessage(message)  # Update status message

    def clear_status(self):
        self.clearMessage()  # Clear status message