from datetime import datetime

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