# Ax8 OpenCV Project

## Overview
Ax8 OpenCV is a modular application designed for real-time camera operations and face recognition. The project is structured to separate concerns into distinct modules, allowing for efficient management of camera feeds, face recognition, signal processing, and user interface.

## Project Structure
The project is organized into the following directories and files:

```
Ax8_OpenCV
├── src
│   ├── camera
│   │   ├── __init__.py
│   │   ├── camera_controller.py
│   │   └── heartbeat.py
│   ├── face_recognition
│   │   ├── __init__.py
│   │   └── recognition_worker.py
│   ├── signal_processing
│   │   ├── __init__.py
│   │   └── signal_handler.py
│   ├── ui
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── camera_widget.py
│   │   └── status_bar.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── signal_manager.py
│   └── app.py
├── requirements.txt
└── README.md
```

## Modules

### Camera Module
- **camera_controller.py**: Manages camera operations, including starting and stopping the camera.
- **heartbeat.py**: Handles the camera's heartbeat signals to ensure operational status.

### Face Recognition Module
- **recognition_worker.py**: Performs face recognition in a separate thread and emits signals for detected faces.

### Signal Processing Module
- **signal_handler.py**: Processes signals from the camera and face recognition threads to ensure smooth operation.

### UI Module
- **main_window.py**: Sets up the main application window and connects UI elements to respective signals.
- **camera_widget.py**: Displays the camera feed and handles UI updates.
- **status_bar.py**: Displays application status and relevant information.

### Utility Module
- **signal_manager.py**: Manages signals between different threads for efficient communication.

## Installation
To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage
To run the application, execute the following command:

```
python src/app.py
```

This will initialize the application, set up the main window, and start the threads for camera operations, face recognition, and signal processing.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.