Object Detection and Communication with Arduino
This project involves detecting objects of specific colors using OpenCV, capturing video from an ESP32-CAM, and sending the detected objects' information to an Arduino via serial communication. The system detects red, blue, and green objects, processes the largest detected contour, and sends the object's color and position data to the Arduino.

Table of Contents
Requirements
Installation
Usage

Requirements
Python 3.x
OpenCV
NumPy
PySerial
ESP32-CAM
Arduino

Installation
Python and Dependencies
Install the required Python packages:

pip install opencv-python numpy pyserial
Setting up ESP32-CAM
Flash the ESP32-CAM with the appropriate firmware to stream video. You can use the example code from the ESP32 Camera Web Server in the Arduino IDE.

Connect the ESP32-CAM to your local network and note its IP address.

Setting up Arduino
Upload the following code to your Arduino to receive data via serial communication:

void setup() {
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        String data = Serial.readStringUntil('\n');
        Serial.println("Received: " + data);
        // Process the received data
    }
}
Usage
Modify the Python script to use your ESP32-CAM's IP address and the correct serial port for your Arduino:

cap = cv2.VideoCapture('http://YOUR_ESP32_CAM_IP:81/stream')
arduino = serial.Serial('COM8', 9600)  # Replace with your Arduino port
Run the Python script:

python object_detection_arduino.py
Control the script:

The script continuously captures frames from the ESP32-CAM and detects objects.
Press w to send the detected objects' data to Arduino.
Press q to quit the script.
