from src.ui.main_window import MainWindow
from src.camera.camera_controller import CameraController
from src.face_recognition.recognition_worker import RecognitionWorker
from src.signal_processing.signal_handler import SignalHandler
from src.utils.signal_manager import SignalManager
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread
import sys

class App:
    def __init__(self, url, username, password):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow(url, username, password)

        # 啟動應用程式
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    # Replace with actual camera URL, username, and password
    camera_url = "http://example.com/camera"
    username = "user"
    password = "pass"
    
    app = App(camera_url, username, password)
    app.run()