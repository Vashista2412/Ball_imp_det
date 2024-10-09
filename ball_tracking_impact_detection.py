import cv2
import pickle
import numpy as np
import imutils
import time
from collections import deque

calib_pts = []
buff_size = 64
yellowLower = (20, 100, 120)  # Range for yellow color ball
yellowUpper = (40, 255, 255)
pts = deque(maxlen=buff_size)

#for a specified frame to be taken, we are taking calibrated frame and the output results in the only frame that we've selected manually as the frame

def mousePoints(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        calib_pts.append((x, y))
        print(f"Point selected: ({x}, {y})")

def calibrate_wall(camera):
    print("Please select the four corners of the wall (Top-Left, Top-Right, Bottom-Left, Bottom-Right)") #need to follow this order in choosing points
    
    ret, frame = camera.read()
    if not ret:
        print("Failed to grab frame for calibration.")
        return None

    while len(calib_pts) < 4: # on the calibrated image frame, we'll mark 4 points as warped frame(chosen frame)
        cv2.imshow("Calibration", frame)
        cv2.setMouseCallback("Calibration", mousePoints)
        cv2.waitKey(1)

    cv2.destroyWindow("Calibration")

    print(f"Selected Points: {calib_pts}")
    with open("calib_data.pkl", 'wb') as f:
        pickle.dump(calib_pts, f)

    return calib_pts

camera = cv2.VideoCapture(0)  # Start webcam
time.sleep(1)

calib_pts = calibrate_wall(camera)

if calib_pts is None:
    print("Calibration failed or not completed. Exiting.")
    camera.release()
    cv2.destroyAllWindows()
    exit()

tl, tr, bl, br = calib_pts

output_width = 600
output_height = 400

dst_pts = np.array([[0, 0], [output_width - 1, 0], [0, output_height - 1], [output_width - 1, output_height - 1]], dtype="float32")

perspective_matrix = cv2.getPerspectiveTransform(np.array([tl, tr, bl, br], dtype="float32"), dst_pts)

previous_center = None  # Initializing
last_impt_pt = None
direc_hist = deque(maxlen=3)  # Check past 3 directions
impt_count = 0
start_time = time.time()
frame_count = 0

impact_points = [] # List to store detected impact points

def draw_impt_pt(frame, pt):
    cv2.circle(frame, pt, 10, (0, 0, 255), -1)  # Draw the impact point
    cv2.putText(frame, f"Impact: {pt}", (pt[0] + 10, pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

last_impact_time = 0  # Track the time of the last valid impact

def detect_impt(direc_hist):
    direc_list = list(direc_hist)
    if len(direc_list) == 3:  # For every 3 frames, check the change of direction
        if direc_list[-1] == "backward" and "forward" in direc_list[:-1]:
            return True
    return False

while True:
    total_time = time.time() - start_time
    if total_time > 40:  # certain time so that it won't run too long
        print("The end!")
        break

    (grabbed, frame) = camera.read()
    if not grabbed:
        break

    frame = imutils.resize(frame, width=600)
    
    warped_frame = cv2.warpPerspective(frame, perspective_matrix, (output_width, output_height))  # Warp the frame to only show the selected area
    
    blurred = cv2.GaussianBlur(warped_frame, (11, 11), 0) # Processing on the warped frame
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, yellowLower, yellowUpper)  # Detect yellow ball
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        moments = cv2.moments(c)  
        if moments["m00"] > 0:
            center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))

        if radius > 0.2:  # Detect smaller yellow balls
            cv2.circle(warped_frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(warped_frame, center, 5, (0, 0, 255), -1)  # Draw center of the ball

            frame_count += 1
            if frame_count % 3 == 0:
                if previous_center is not None:
                    if center[1] < previous_center[1]:
                        curr_direc = "forward"  # Ball is moving upward
                    else:
                        curr_direc = "backward"  # Ball is moving downward

                    direc_hist.append(curr_direc)

                    if detect_impt(direc_hist):
                        curr_time = time.time()
                        # Ensure that at least 0.8 seconds have passed since the last impact
                        if curr_time - last_impact_time >= 0.8:
                            if last_impt_pt is None or (abs(center[0] - last_impt_pt[0]) > 5 and abs(center[1] - last_impt_pt[1]) > 5):
                                impt_count += 1
                                print(f"Impact {impt_count} detected at {center}.")  # Print the impact point
                                impact_points.append((center, curr_time))  # Store the impact point and time
                                draw_impt_pt(warped_frame, center)
                                cv2.putText(warped_frame, "Impact Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                                last_impt_pt = center
                                last_impact_time = curr_time  # Update the last impact time

                previous_center = center

    curr_time = time.time()
    for pt, timestamp in impact_points:
        if curr_time - timestamp < 5:  # Keep impact point visible for 5 seconds
            draw_impt_pt(warped_frame, pt)

    pts.appendleft(center)
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = int(np.sqrt(buff_size / float(i + 1)) * 2.5)
        cv2.line(warped_frame, pts[i - 1], pts[i], (0, 255, 0), thickness)

    cv2.imshow("Warped Frame", warped_frame) # showing the warped frame and mask
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
