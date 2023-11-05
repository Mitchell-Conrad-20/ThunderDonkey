import cv2
import numpy as np

# Define the HSV color ranges for red
lower_red = np.array([0, 100, 100])  # Lower bound for red in HSV
upper_red = np.array([10, 255, 255])  # Upper bound for red in HSV

# Load the video
video_path = 'C:\\Users\\james\\Desktop\\Hackathon_2023\\Videos\\killed.mp4'  # Replace with the path to your video file
cap = cv2.VideoCapture(video_path)

total_contour_area = 0  # Variable to store the total contour area

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask to detect red color within the defined HSV range
    mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original frame
    contour_image = frame.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 0, 255), 2)  # Red color, thickness 2
    total_contour_area = 0
    # Calculate and sum the area of each contour
    for contour in contours:
        total_contour_area += cv2.contourArea(contour)
    if total_contour_area > 330516:
        print(total_contour_area)
    # Display the total contour area
    cv2.putText(contour_image, f'Total Contour Area: {total_contour_area}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame with contours and total area
    cv2.imshow('Video with Contours and Total Area', contour_image)

    if cv2.waitKey(25) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()

print("Total Contour Area:", total_contour_area)  # Print the total area when the video processing is finished
