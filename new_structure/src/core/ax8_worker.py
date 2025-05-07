from PyQt5.QtCore import QObject, pyqtSignal
from src.core.ax8_manager import AX8Manager

class AX8Worker(QObject):
    image_update = pyqtSignal(object)  # 傳遞影像資料的信號
    connection_status = pyqtSignal(str)  # 傳遞連線狀態的信號

    def __init__(self, url, username, password):
        super().__init__()
        self.url = url
        self.username = username
        self.password = password
        self.manager = AX8Manager(url, username, password)
        self.running = False

    def start(self):
        try:
            if self.manager.login():
                self.connection_status.emit("Connected")
                print("[AX8Worker] 登錄成功，開始顯示影像串流")
                self.running = True
                self.manager.display_stream(self.update_image)
            else:
                self.connection_status.emit("Connection Failed")
                print("[AX8Worker] 登錄失敗，無法顯示影像串流")
        except Exception as e:
            print(f"[AX8Worker] 發生錯誤: {e}")
        finally:
            self.stop()

    def update_image(self, image):
        """更新影像並發送信號"""
        self.image_update.emit(image)

    def stop(self):
        """停止影像串流並釋放資源"""
        if self.running:
            self.manager.stop()
            self.running = False
            print("[AX8Worker] 已停止影像串流")