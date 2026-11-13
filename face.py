import cv2
import face_recognition
import numpy as np
import serial
import time
import requests

SERVER_URL = "http://192.168.1.109:5000/update"  # Replace <server-ip> with the Flask server's IP address


# Initialize the serial communication with the Arduino
try:
    arduino = serial.Serial('COM3', baudrate=9600, timeout=1)  
    time.sleep(2)  # Wait for the serial connection to initialize
    print("Connected")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Load known face image
known_face_name = "younes"  # Replace with your name
try:
    face_image = face_recognition.load_image_file("your_face.jpg")
    known_face_encoding = face_recognition.face_encodings(face_image)[0]
    print("Loaded known face encoding.")
except Exception as e:
    print(f"Error loading face image: {e}")
    exit()

# Initialize the webcam
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

print("Face recognition system started. Press 'q' to quit.")

while True:
    try:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Failed to capture image from webcam.")
            break

        rgb_frame = frame[:, :, ::-1]
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_detected = False
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([known_face_encoding], face_encoding, tolerance=0.6)
            if True in matches:
                face_detected = True
                break

        # Send signal to server
        command = "1" if face_detected else "0"
        response = requests.post(SERVER_URL, json={"command": command})
        if response.status_code == 200:
            print(f"Server updated with command: {command}")
        else:
            print("Failed to update server.")

        # Your existing video display code...

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting the program.")
            break

    except Exception as e:
        print(f"Error in processing: {e}")
        continue

video_capture.release()
cv2.destroyAllWindows()
arduino.close()