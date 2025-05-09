from PyQt5.QtCore import QObject, pyqtSignal, QThread
import cv2

class RecognitionWorker(QObject):
    face_detected_signal = pyqtSignal(object)  # Signal to emit detected faces
    detection_feed_signal = pyqtSignal(object)  # Signal to emit detection feed
    fps_signal = pyqtSignal(float)  # Signal to emit FPS
    inference_time_signal = pyqtSignal(float)  # Signal to emit inference time

    def __init__(self, signal_manager):
        super().__init__()
        self.signal_manager = signal_manager  # 儲存 signal_manager
        self.running = False
        self.capture = None

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
        if self.capture is not None:
            self.capture.release()

    def run(self):
        self.capture = cv2.VideoCapture(0)  # Open the default camera
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                # Perform face detection (dummy implementation)
                faces = self.detect_faces(frame)
                if faces:
                    self.signal_manager.face_recognition_signal.emit(faces)
                    self.signal_manager.frame_signal.emit(frame)
                # Emit FPS and inference time (dummy values)
                self.signal_manager.fps_signal.emit(30.0)
                self.signal_manager.inference_time_signal.emit(100.0)

    def detect_faces(self, frame):
        # Dummy face detection logic
        # In a real implementation, you would use a face detection model here
        return []  # Return detected faces (empty for now)