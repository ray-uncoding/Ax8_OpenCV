from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
import cv2
from ax8_legcy.ax8_manager import AX8Manager
import time
from ..utils.data_processor import FPSCounter
import csv
import os
from datetime import datetime

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

        self.fps_counter = FPSCounter()  # 初始化 FPS 計算器
        self.log_file = os.path.join(os.getcwd(), "parameter_log.csv")  # 記錄檔案路徑
        self.init_log_file()  # 初始化記錄檔案

    def init_log_file(self):
        """初始化記錄檔案，寫入標題行"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "FPS", "Inference Time (ms)"])  # 標題行

    def log_parameters(self, fps, inference_time):
        """記錄參數到 CSV 文件"""
        with open(self.log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, f"{fps:.2f}", f"{inference_time:.2f}"])

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

                # 使用 FPSCounter 計算 FPS
                fps = self.fps_counter.update()
                self.fps_signal.emit(fps)

                # 記錄參數變化
                self.log_parameters(fps, results[0].speed['inference'])
        except Exception as e:
            print(f"[CameraWidget] 更新畫面時發生錯誤: {e}")

    def stop_camera(self):
        self.timer.stop()
        self.ax8_manager.stop()
        self.image_label.clear()