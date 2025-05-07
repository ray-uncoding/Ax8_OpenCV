from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
import cv2
from ax8_legcy.ax8_manager import AX8Manager
import time

class CameraWidget(QWidget):
    detection_feed_signal = pyqtSignal(QPixmap)
    fps_signal = pyqtSignal(float)
    inference_time_signal = pyqtSignal(float)

    def __init__(self, url, username, password, parent=None):
        super(CameraWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

        self.ax8_manager = AX8Manager(url, username, password)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # 初始化 FPS 計算
        self.frame_count = 0
        self.start_time = time.time()

    def start_camera(self):
        if self.ax8_manager.login():
            self.timer.start(30)  # 每 30 毫秒更新一次畫面
        else:
            print("Failed to connect to AX8 camera.")

    def update_frame(self):
        try:
            frame = self.ax8_manager.fetch_frame()
            if frame is not None:
                # 原始畫面
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(q_img))

                # YOLO 偵測
                results = self.ax8_manager.model.predict(frame)
                detection_frame = results[0].plot()  # 繪製偵測結果
                detection_rgb = cv2.cvtColor(detection_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = detection_rgb.shape
                bytes_per_line = ch * w
                detection_q_img = QImage(detection_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                detection_pixmap = QPixmap.fromImage(detection_q_img)

                # 發送信號更新 UI
                self.detection_feed_signal.emit(detection_pixmap)
                self.inference_time_signal.emit(results[0].speed['inference'])

                # 計算 FPS
                self.frame_count += 1
                elapsed_time = time.time() - self.start_time
                fps = self.frame_count / elapsed_time if elapsed_time > 0 else 0
                self.fps_signal.emit(fps)
        except Exception as e:
            print(f"[CameraWidget] 更新畫面時發生錯誤: {e}")

    def stop_camera(self):
        self.timer.stop()
        self.ax8_manager.stop()
        self.image_label.clear()