# Ball Tracking and Impact Detection

This project uses OpenCV to track a yellow ball in real-time via a webcam and detect impacts based on the ball’s change of direction. It applies a perspective transformation on a selected region of the frame, processes the movement, and highlights any impact events detected.

## Features

- **Real-time Video Processing**: Captures video from the webcam and processes each frame.
- **Ball Detection**: Detects and tracks a yellow ball using HSV color space filtering.
- **Impact Detection**: Identifies impact events when the ball changes direction sharply.
- **Perspective Calibration**: Allows the user to manually select a region of interest (ROI) by specifying four points (Top-Left, Top-Right, Bottom-Left, Bottom-Right) on the video feed.
- **Visual Feedback**: Displays the tracked ball, its trail, and the detected impact points on the frame.
- **Configurable**: The HSV range and detection parameters can be customized for different lighting conditions or objects.

## Requirements

To run this project, you need the following dependencies:

- Python 3.x
- OpenCV
- NumPy
- Imutils

Install the required dependencies using pip:

```bash
pip install numpy opencv-python imutils

To clone the repo, open the terminal and run the following command
```bash
git clone https://github.com/Vashista2412/Ball_imp_det

To run the script

