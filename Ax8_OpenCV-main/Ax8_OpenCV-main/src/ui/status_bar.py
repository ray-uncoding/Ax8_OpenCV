from PyQt5.QtWidgets import QStatusBar, QLabel, QHBoxLayout, QWidget

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        
        self.connection_status_label = QLabel("Connection Status: Disconnected")
        self.fps_label = QLabel("FPS: 0")
        self.detection_params_label = QLabel("Detection Params: N/A")
        
        self.layout.addWidget(self.connection_status_label)
        self.layout.addWidget(self.fps_label)
        self.layout.addWidget(self.detection_params_label)
        
        self.setLayout(self.layout)

    def update_connection_status(self, status):
        self.connection_status_label.setText(f"Connection Status: {status}")

    def update_fps(self, fps):
        self.fps_label.setText(f"FPS: {fps}")

    def update_detection_params(self, params):
        self.detection_params_label.setText(f"Detection Params: {params}")