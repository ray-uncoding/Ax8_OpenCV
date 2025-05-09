from PyQt5.QtCore import pyqtSignal, QObject
import cv2
import time

class CameraController(QObject):
    camera_started = pyqtSignal()
    camera_stopped = pyqtSignal()
    frame_signal = pyqtSignal(object)  # Signal to send frames to UI
    heartbeat_signal = pyqtSignal(bool)  # Signal to indicate camera status

    def __init__(self, url, username, password, signal_manager):
        super().__init__()
        self.url = url
        self.username = username
        self.password = password
        self.signal_manager = signal_manager  # 傳遞 signal_manager
        self.capture = None
        self.running = False

    def start_camera(self):
        if not self.running:
            self.capture = cv2.VideoCapture(self.url)
            if self.capture.isOpened():
                self.running = True
                self.signal_manager.camera_started.emit()
                self.process_camera_frames()

    def stop_camera(self):
        if self.running:
            self.running = False
            self.capture.release()
            self.signal_manager.camera_stopped.emit()

    def process_camera_frames(self):
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                self.frame_signal.emit(frame)
            else:
                self.heartbeat_signal.emit(False)
            time.sleep(0.03)  # Simulate frame processing delay

    def is_camera_running(self):
        return self.running