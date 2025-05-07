from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from .camera_widget import CameraWidget
from .status_bar import StatusBar

class MainWindow(QMainWindow):
    def __init__(self, url, username, password):
        super(MainWindow, self).__init__()
        self.setWindowTitle("AX8 Camera Interface")
        self.setGeometry(100, 100, 1200, 600)  # 調整視窗大小

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主佈局
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # 左側：原始相機畫面
        self.camera_widget = CameraWidget(url, username, password)
        self.main_layout.addWidget(self.camera_widget)

        # 右側：人物辨識畫面
        self.detection_label = QLabel("Detection Feed")
        self.detection_label.setAlignment(Qt.AlignCenter)
        self.detection_label.setStyleSheet("background-color: #000; color: #FFF;")
        self.detection_label.setScaledContents(False)  # 禁用內容縮放，改用手動縮放
        self.main_layout.addWidget(self.detection_label)

        # 下方：參數顯示區域
        self.bottom_layout = QVBoxLayout()
        self.main_layout.addLayout(self.bottom_layout)

        self.fps_label = QLabel("FPS: N/A")
        self.inference_label = QLabel("Inference Time: N/A")
        self.bottom_layout.addWidget(self.fps_label)
        self.bottom_layout.addWidget(self.inference_label)

        # 控制按鈕
        self.start_button = QPushButton("Start Camera")
        self.start_button.clicked.connect(self.camera_widget.start_camera)
        self.bottom_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Camera")
        self.stop_button.clicked.connect(self.camera_widget.stop_camera)
        self.bottom_layout.addWidget(self.stop_button)

        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

        # 連接信號
        self.camera_widget.detection_feed_signal.connect(self.update_detection_feed)
        self.camera_widget.fps_signal.connect(self.update_fps)
        self.camera_widget.inference_time_signal.connect(self.update_inference_time)

    def update_fps(self, fps):
        if fps is not None:
            self.fps_label.setText(f"FPS: {fps:.2f}")

    def update_inference_time(self, time_ms):
        if time_ms is not None:
            self.inference_label.setText(f"Inference Time: {time_ms:.2f} ms")

    def update_detection_feed(self, pixmap):
        if pixmap is not None:
            # 縮放影像以保持寬高比
            scaled_pixmap = pixmap.scaled(
                self.detection_label.size(),  # QLabel 的大小
                Qt.KeepAspectRatio,          # 保持寬高比
                Qt.SmoothTransformation      # 平滑縮放
            )
            self.detection_label.setPixmap(scaled_pixmap)