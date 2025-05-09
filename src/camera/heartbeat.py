from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class Heartbeat(QObject):
    heartbeat_signal = pyqtSignal(bool)

    def __init__(self, camera_controller, interval=1000):
        super().__init__()
        self.camera_controller = camera_controller
        self.interval = interval
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_camera_status)
        self.timer.start(self.interval)

    def check_camera_status(self):
        is_operational = self.camera_controller.is_camera_operational()
        self.heartbeat_signal.emit(is_operational)