from PyQt5.QtCore import QObject, pyqtSignal

class SignalManager(QObject):
    # Define signals for communication between threads
    camera_signal = pyqtSignal(object)  # Signal for camera data
    face_recognition_signal = pyqtSignal(object)  # Signal for face recognition results
    processed_signal = pyqtSignal(object)  # Signal for processed data
    frame_signal = pyqtSignal(object)
    fps_signal = pyqtSignal(float)
    inference_time_signal = pyqtSignal(float)
    camera_started = pyqtSignal()
    camera_stopped = pyqtSignal()