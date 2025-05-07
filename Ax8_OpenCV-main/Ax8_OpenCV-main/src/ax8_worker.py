from ax8_manager import AX8Manager
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QObject

class WorkerSignals(QObject):
    image_update = pyqtSignal(object)
    connection_status = pyqtSignal(str)
    fps_update = pyqtSignal(int)

class AX8Worker(threading.Thread):
    def __init__(self, url, username, password):
        super().__init__()
        self.url = url
        self.username = username
        self.password = password
        self.manager = AX8Manager(url, username, password)
        self.signals = WorkerSignals()

    def run(self):
        try:
            if self.manager.login():
                self.signals.connection_status.emit("Connected")
                print("[AX8Worker] 登錄成功，開始顯示影像串流")
                self.manager.display_stream(self.update_image)
            else:
                self.signals.connection_status.emit("Connection Failed")
                print("[AX8Worker] 登錄失敗，無法顯示影像串流")
        except KeyboardInterrupt:
            print("[AX8Worker] 停止 Worker")
        finally:
            self.manager.stop()

    def update_image(self, image):
        self.signals.image_update.emit(image)
        # Here you would calculate and emit the FPS as well
        # self.signals.fps_update.emit(calculated_fps)

if __name__ == "__main__":
    AX8_URL = "http://192.168.1.100/snapshot.jpg"
    USERNAME = "admin"
    PASSWORD = "admin"

    app = QApplication([])
    worker = AX8Worker(AX8_URL, USERNAME, PASSWORD)
    worker.start()
    app.exec_()