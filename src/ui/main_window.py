from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from src.ui.camera_widget import CameraWidget
from src.ui.status_bar import StatusBar
from src.utils.signal_manager import SignalManager
from src.camera.camera_controller import CameraController
from src.face_recognition.recognition_worker import RecognitionWorker
from src.signal_processing.signal_handler import SignalHandler
from PyQt5.QtCore import QThread

class MainWindow(QMainWindow):
    def __init__(self, url, username, password):
        super().__init__()
        self.signal_manager = SignalManager()

        # 初始化 SignalHandler 並傳遞 signal_manager
        self.signal_handler = SignalHandler(self.signal_manager)
        self.signal_thread = QThread()
        self.signal_handler.moveToThread(self.signal_thread)

        # 啟動執行緒
        self.signal_thread.start()

        # 初始化其他元件
        self.camera_controller = CameraController(url, username, password, self.signal_manager)
        self.recognition_worker = RecognitionWorker(self.signal_manager)

        self.setup_connections()

        self.setWindowTitle("AX8 Camera Interface")
        self.setGeometry(100, 100, 1200, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.camera_widget = CameraWidget(url, username, password)
        self.main_layout.addWidget(self.camera_widget)

        self.detection_label = QLabel("Detection Feed")
        self.detection_label.setAlignment(Qt.AlignCenter)
        self.detection_label.setStyleSheet("background-color: #000; color: #FFF;")
        self.detection_label.setScaledContents(False)
        self.main_layout.addWidget(self.detection_label)

        self.bottom_layout = QVBoxLayout()
        self.main_layout.addLayout(self.bottom_layout)

        self.fps_label = QLabel("FPS: N/A")
        self.inference_label = QLabel("Inference Time: N/A")
        self.bottom_layout.addWidget(self.fps_label)
        self.bottom_layout.addWidget(self.inference_label)

        self.start_button = QPushButton("Start Camera")
        self.start_button.clicked.connect(self.start_camera)
        self.bottom_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Camera")
        self.stop_button.clicked.connect(self.stop_camera)
        self.bottom_layout.addWidget(self.stop_button)

        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

        self.camera_thread = QThread()
        self.recognition_thread = QThread()

        self.camera_controller.moveToThread(self.camera_thread)
        self.recognition_worker.moveToThread(self.recognition_thread)

        # 啟動執行緒
        self.recognition_thread.started.connect(self.recognition_worker.run)
        self.recognition_thread.start()

    def setup_connections(self):
        # 訊號連接
        self.signal_manager.frame_signal.connect(self.signal_handler.process_camera_signal)
        self.signal_manager.face_recognition_signal.connect(self.signal_handler.process_recognition_signal)
        self.signal_handler.detection_signal.connect(self.update_detection_feed)
        self.signal_handler.fps_signal.connect(self.update_fps)
        self.signal_handler.inference_time_signal.connect(self.update_inference_time)

    def start_camera(self):
        self.camera_thread.start()
        self.camera_controller.start_camera()

    def stop_camera(self):
        self.camera_controller.stop_camera()
        self.camera_thread.quit()
        self.camera_thread.wait()

    def update_fps(self, fps):
        if fps is not None:
            self.fps_label.setText(f"FPS: {fps:.2f}")

    def update_inference_time(self, time_ms):
        if time_ms is not None:
            self.inference_label.setText(f"Inference Time: {time_ms:.2f} ms")

    def update_detection_feed(self, pixmap):
        if pixmap is not None:
            scaled_pixmap = pixmap.scaled(
                self.detection_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.detection_label.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        # 停止執行緒
        self.camera_controller.stop_camera()
        self.camera_thread.quit()
        self.camera_thread.wait()

        self.recognition_worker.stop()
        self.recognition_thread.quit()
        self.recognition_thread.wait()

        self.signal_thread.quit()
        self.signal_thread.wait()

        super().closeEvent(event)