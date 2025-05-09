from PyQt5.QtCore import QObject, pyqtSignal

class SignalHandler(QObject):
    detection_signal = pyqtSignal(object)  # Signal to emit detected faces
    fps_signal = pyqtSignal(float)          # Signal to emit FPS updates
    inference_time_signal = pyqtSignal(float)  # Signal to emit inference time updates

    def __init__(self, signal_manager):
        super().__init__()
        self.signal_manager = signal_manager  # 儲存 signal_manager