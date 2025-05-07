# AX8 Camera Project

## Overview
The AX8 Camera Project is a PyQt-based application designed to interface with the AX8 camera system. It provides a user-friendly interface for displaying the camera feed, monitoring connection status, and showcasing parameters related to a person detection system.

## Project Structure
```
ax8_project
├── src
│   ├── ax8_worker.py          # Manages camera connection and image streaming
│   ├── ui
│   │   ├── main_window.py      # Main window of the application
│   │   ├── camera_widget.py     # Widget for displaying camera feed
│   │   └── status_bar.py       # Status bar showing connection and detection info
│   ├── utils
│   │   └── data_processor.py   # Utility functions for data processing
│   └── resources
│       └── styles.qss          # Stylesheet for UI components
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── main.py                     # Entry point for the application
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ax8_project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python main.py
```

This will launch the PyQt application, allowing you to connect to the AX8 camera and view the live feed along with relevant data.

## Features
- **Camera Feed Display**: Real-time video stream from the AX8 camera.
- **Connection Status**: Visual indicators for camera connection status.
- **FPS Monitoring**: Displays frames per second for the video stream.
- **Person Detection Parameters**: Shows relevant parameters from the person detection system.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.