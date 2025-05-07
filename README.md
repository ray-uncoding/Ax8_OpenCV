# AX8 Camera Project

## Overview
The AX8 Camera Project is a PyQt-based application designed to interface with the AX8 camera system. It provides a modular and extensible architecture for real-time video streaming, object detection, and system monitoring. The project leverages PyQt for the user interface, YOLO for object detection, and utility modules for data processing and logging.

---

## Project Structure
```
ax8_project
├── main.py                     # Entry point for the application
├── src
│   ├── config
│   │   └── yolov8n.pt          # YOLO model file
│   ├── core
│   │   ├── ax8_manager.py      # Manages camera connection, image fetching, and session handling
│   │   ├── ax8_worker.py       # Handles threaded operations for image streaming
│   │   ├── yolo_processor.py   # Encapsulates YOLO model for object detection
│   ├── ui
│   │   ├── main_window.py      # Main application window
│   │   ├── camera_widget.py    # Widget for displaying camera feed and detection results
│   │   └── status_bar.py       # Status bar showing connection and detection info
│   ├── utils
│   │   ├── data_processor.py   # Utility for FPS calculation
│   │   ├── logger.py           # Configurable logging setup
│   │   └── parameter_logger.py # Logs detection parameters to a CSV file
│   └── resources
│       └── styles.qss          # Stylesheet for UI components
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ax8_project
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

---

## Usage

To run the application, execute the following command:
```bash
python main.py
```

This will launch the PyQt application, allowing you to connect to the AX8 camera and view the live feed along with relevant data.

---

## System Architecture and Workflow

### **1. Camera Connection and Image Fetching**
- **Module**: `ax8_manager.py`
- **Description**: 
  - Manages the connection to the AX8 camera.
  - Handles login, image fetching, and session keep-alive through a dedicated thread.
- **Key Methods**:
  - `login()`: Authenticates with the camera.
  - `fetch_frame()`: Fetches the latest frame from the camera.
  - `start_keep_alive()`: Maintains the session by sending periodic requests.

### **2. Image Streaming and Processing**
- **Module**: `ax8_worker.py`
- **Description**: 
  - Runs a threaded worker to fetch frames continuously.
  - Emits signals to update the UI with the latest frames and connection status.
- **Key Signals**:
  - `image_update`: Sends the latest frame to the UI.
  - `connection_status`: Updates the connection status in the status bar.

### **3. YOLO Object Detection**
- **Module**: `yolo_processor.py`
- **Description**: 
  - Encapsulates the YOLO model for object detection.
  - Processes each frame to detect objects and returns detection results.
- **Key Method**:
  - `predict(frame)`: Runs YOLO inference on the given frame.

### **4. User Interface**
- **Modules**: `main_window.py`, `camera_widget.py`, `status_bar.py`
- **Description**:
  - **`main_window.py`**: The main application window that integrates all UI components.
  - **`camera_widget.py`**: Displays the camera feed and overlays detection results.
  - **`status_bar.py`**: Shows connection status, FPS, and detection parameters.
- **Workflow**:
  1. `CameraWidget` fetches frames from `AX8Worker`.
  2. Frames are passed to `YOLOProcessor` for detection.
  3. Detection results are displayed on the UI.

### **5. Utility Modules**
- **Modules**: `data_processor.py`, `logger.py`, `parameter_logger.py`
- **Description**:
  - **`data_processor.py`**: Calculates FPS for the video stream.
  - **`logger.py`**: Configures logging for debugging and monitoring.
  - **`parameter_logger.py`**: Logs detection parameters (e.g., FPS, inference time) to a CSV file.

---

## Features

### **1. Real-Time Camera Feed**
- Displays a live video stream from the AX8 camera.
- Supports real-time object detection using YOLO.

### **2. Connection Monitoring**
- Visual indicators for connection status.
- Automatic session keep-alive to prevent disconnection.

### **3. FPS Monitoring**
- Calculates and displays frames per second for the video stream.

### **4. Object Detection**
- Integrates YOLO for detecting objects in the video stream.
- Displays detection results (e.g., bounding boxes, labels) on the video feed.

### **5. Parameter Logging**
- Logs FPS and inference time to a CSV file for performance analysis.

---

## Development Notes

### **1. Adding a New YOLO Model**
- Update the `YOLOProcessor` class with the new model path.
- Ensure the model is compatible with the `ultralytics` library.

### **2. Debugging**
- Use the `logger.py` module to enable detailed logging.
- Logs are stored in a rotating file to prevent excessive disk usage.

### **3. Extending the System**
- To support multiple cameras:
  - Instantiate multiple `AX8Manager` and `CameraWidget` objects.
  - Use a tabbed interface in `main_window.py` to switch between cameras.

---

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

---

## License
This project is licensed under the MIT License. See the LICENSE file for more details.