from PyQt5.QtCore import QObject, pyqtSignal

class SignalHandler(QObject):
    detection_signal = pyqtSignal(object)  # Signal to emit detected faces
    fps_signal = pyqtSignal(float)         # Signal to emit FPS updates
    inference_time_signal = pyqtSignal(float)  # Signal to emit inference time updates

    def __init__(self, signal_manager):
        super().__init__()
        self.signal_manager = signal_manager  # 儲存 signal_manager

    def process_camera_signal(self, frame):
        # 處理來自相機的訊號
        print("Processing camera frame...")
        self.detection_signal.emit(frame)  # 假設處理後發送 detection_signal

    def process_recognition_signal(self, recognition_data):
        # 處理來自人臉辨識的訊號
        print("Processing recognition data...")
        # 假設這裡進行一些處理後，發送其他訊號