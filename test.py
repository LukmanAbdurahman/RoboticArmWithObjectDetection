import cv2
import numpy as np
import serial

# Basic constants for OpenCV functions
kernel = np.ones((3, 3), 'uint8')
font = cv2.FONT_HERSHEY_SIMPLEX 
fontScale = 0.6 
thickness = 2

# Initialize serial communication with Arduino
# Replace 'COM8' with your Arduino port
arduino = serial.Serial('COM8', 9600)

# Extract Frames 
# Replace the URL with your ESP32-CAM's IP address and stream port
cap = cv2.VideoCapture('http://192.168.43.196:81/stream')

cv2.namedWindow('Object Color Detection', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Object Color Detection', 600, 600)

# Loop to capture video frames
data_to_send = []
while True:
    ret, img = cap.read()
    if not ret:
        break

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range of red color in HSV
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    # Define range of blue color in HSV
    lower_blue = np.array([90, 70, 50])
    upper_blue = np.array([130, 255, 255])

    # Define range of green color in HSV
    lower_green = np.array([35, 70, 50])
    upper_green = np.array([85, 255, 255])

    # Threshold the HSV images to get only red, blue, and green colors
    mask_red1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)
    
    mask_green = cv2.inRange(hsv_img, lower_green, upper_green)

    # Remove extra noise from images
    d_img_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel, iterations=5)
    d_img_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel, iterations=5)
    d_img_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel, iterations=5)

    # Find contours for red objects
    contours_red, _ = cv2.findContours(d_img_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red = sorted(contours_red, key=cv2.contourArea, reverse=True)

    # Find contours for blue objects
    contours_blue, _ = cv2.findContours(d_img_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue = sorted(contours_blue, key=cv2.contourArea, reverse=True)
    
    # Find contours for green objects
    contours_green, _ = cv2.findContours(d_img_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green = sorted(contours_green, key=cv2.contourArea, reverse=True)

    # List to hold all contours with color information
    all_contours = []

    for cnt in contours_red:
        if 100 < cv2.contourArea(cnt) < 306000:
            all_contours.append((cnt, 'Merah', (0, 0, 255)))
    
    for cnt in contours_blue:
        if 100 < cv2.contourArea(cnt) < 306000:
            all_contours.append((cnt, 'Biru', (255, 0, 0)))
    
    for cnt in contours_green:
        if 100 < cv2.contourArea(cnt) < 306000:
            all_contours.append((cnt, 'Hijau', (0, 255, 0)))

    # Sort contours by area (largest to smallest)
    all_contours = sorted(all_contours, key=lambda x: cv2.contourArea(x[0]), reverse=True)

    # Process only the largest contour
    if all_contours:
        cnt, color, color_code = all_contours[0]
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.array(box, dtype=int)
        cv2.drawContours(img, [box], 0, color_code, 3)

        # Get the center of the box
        center = (int(rect[0][0]), int(rect[0][1]))
        cv2.circle(img, center, 5, color_code, -1)
        
        # Display color and number detected in the box
        cv2.putText(img, f'{color} 1', (box[0][0], box[0][1] - 10), font, fontScale, color_code, thickness, cv2.LINE_AA)
        
        # Add to data to send
        data_to_send = [f'{color.lower()}1']
        
        # Create the data string to send
        data_string = ','.join(data_to_send)
    else:
        data_string = ''

    # Display the data to be sent on the screen
    cv2.putText(img, f'Data to send: {data_string}', (10, 60), font, fontScale, (255, 255, 255), thickness, cv2.LINE_AA)
    
    # Display the total number of objects detected
    cv2.putText(img, f'Jumlah objek: {1 if all_contours else 0}', (10, 30), font, fontScale, (255, 255, 255), thickness, cv2.LINE_AA)

    cv2.imshow('Object Color Detection', img)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('w'):  # Enter key
        if data_string:
            arduino.write(data_string.encode())
            arduino.flush()
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
