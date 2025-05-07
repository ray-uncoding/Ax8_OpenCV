import time
from datetime import datetime

class FPSCounter:
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0

    def update(self):
        """更新幀數並計算 FPS"""
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        return self.frame_count / elapsed_time if elapsed_time > 0 else 0

    def reset(self):
        """重置 FPS 計算"""
        self.start_time = time.time()
        self.frame_count = 0

def calculate_fps(start_time, frame_count):
    """
    Calculate frames per second (FPS).
    
    :param start_time: The time when the video stream started.
    :param frame_count: The number of frames processed.
    :return: Calculated FPS.
    """
    elapsed_time = (datetime.now() - start_time).total_seconds()
    if elapsed_time > 0:
        return frame_count / elapsed_time
    return 0

def format_detection_parameters(detection_data):
    """
    Format detection parameters for display.
    
    :param detection_data: Dictionary containing detection parameters.
    :return: Formatted string of detection parameters.
    """
    formatted_params = []
    for key, value in detection_data.items():
        formatted_params.append(f"{key}: {value}")
    return "\n".join(formatted_params)