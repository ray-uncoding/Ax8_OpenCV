from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, QTimer
from src.core.ax8_manager import AX8Manager
from src.utils.data_processor import FPSCounter
from src.utils.parameter_logger import ParameterLogger  # 引入記錄模組
import cv2
from PyQt5.QtGui import QPixmap, QImage

class CameraWidget(QWidget):
    detection_feed_signal = pyqtSignal(QPixmap)
    fps_signal = pyqtSignal(float)
    inference_time_signal = pyqtSignal(float)

    def __init__(self, url, username, password, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.image_label = QLabel("Camera Feed")
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

        self.ax8_manager = AX8Manager(url, username, password)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.fps_counter = FPSCounter()
        self.logger = ParameterLogger()  # 初始化記錄器

    def start_camera(self):
        if self.ax8_manager.login():
            self.timer.start(30)
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
                detection_frame = results[0].plot()
                detection_rgb = cv2.cvtColor(detection_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = detection_rgb.shape
                bytes_per_line = ch * w
                detection_q_img = QImage(detection_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                detection_pixmap = QPixmap.fromImage(detection_q_img)

                # 發送信號
                self.detection_feed_signal.emit(detection_pixmap)
                self.inference_time_signal.emit(results[0].speed['inference'])

                # 計算 FPS
                fps = self.fps_counter.update()
                self.fps_signal.emit(fps)

                # 記錄參數
                self.logger.log_parameters(fps, results[0].speed['inference'])
        except Exception as e:
            print(f"[CameraWidget] Error updating frame: {e}")

    def stop_camera(self):
        self.timer.stop()
        self.ax8_manager.stop()
        self.image_label.clear()