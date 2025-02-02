from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
frame = picam2.capture_array()

cv2.imwrite("test.jpg", frame)
print("Image captured successfully.")