from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
import sys

def main():
    # AX8 相機參數
    AX8_URL = "http://192.168.1.100/snapshot.jpg"
    USERNAME = "admin"
    PASSWORD = "admin"

    app = QApplication(sys.argv)
    window = MainWindow(AX8_URL, USERNAME, PASSWORD)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()