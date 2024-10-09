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

- Python 
- OpenCV
- NumPy
- Imutils

Install the required dependencies using pip:
```bash
pip install numpy opencv-python imutils
```

To clone the repo, open the terminal and run the following command
```bash
git clone https://github.com/Vashista2412/Ball_imp_det
```

To run the script
```bash
python ball_tracking_impact_detection.py
```

After running the script, the webcam feed will appear, and you will be prompted to select four points on the frame for calibration:

- Top-Left: Click the top-left corner of the area to track.
- Top-Right: Click the top-right corner.
- Bottom-Left: Click the bottom-left corner.
- Bottom-Right: Click the bottom-right corner.

The system tracks the yellow ball, detects when the ball changes direction (indicating a potential impact), and marks the impact point on the frame. 
The program runs for 40 seconds or until you manually stop it.

Manual Exit: Press the q key at any time to exit the program.

If you are tracking an object other than a yellow ball, you can modify the HSV range for detection. These are currently set for yellow but can be updated in the script: <br>
yellowLower = (20, 100, 120) - Lower bound of the HSV range for yellow <br>
yellowUpper = (40, 255, 255) - Upper bound of the HSV range for yellow

You can adjust the size of the warped frame by modifying the output_width and output_height parameters: <br>
output_width = 600 <br>
output_height = 400

## **Expected Results:**
During the execution of the program, the warped frame and the masked image (for ball detection) are shown. Any detected impact points are highlighted in red dot.

## **Troubleshooting**
- If the ball is not being detected, try adjusting the HSV values for more precise color detection.
- Ensure the lighting conditions are stable for accurate detection.
- Use a webcam with good resolution for better tracking accuracy.
- Ensure the camera is placed at a certain height to improve impact calculation
