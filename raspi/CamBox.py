import RPi.GPIO as gp
import os
import time
import cv2
from picamera2 import Picamera2
from flask import Flask, Response, request

gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)
print('GPIO setup complete')

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main = {"size": (640, 480), "format": "BGR888"}, buffer_count=6))

#set register for camera
i2c = "i2cset -y 1 0x70 0x00 0x04"
#set adapter board to correct camera
os.system(i2c)
gp.output(7, False)
gp.output(11, False)
gp.output(12, True)
#allow time for switch
time.sleep(0.5)
picam2.start()
print('On camera A')

print('picam setup complete')

app = Flask(__name__)

def switchCamera(cameraId):
    picam2.close()
    #select correct camera
    if(cameraId == 1):
        
        #set register for camera
        i2c = "i2cset -y 1 0x70 0x00 0x04"
        #set adapter board to correct camera
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)
        #allow time for switch
        time.sleep(0.5)
        picam2.start()
        print('On camera A')
    elif(cameraId == 2):
        i2c = "i2cset -y 1 0x70 0x00 0x05"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, False)
        gp.output(12, True)
        time.sleep(0.5)
        picam2.start()
        print('On camera B') 
    elif(cameraId == 3):
        print('On camera C')
        i2c = "i2cset -y 1 0x70 0x00 0x06"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, True)
        gp.output(12, False)
        time.sleep(0.5)
        picam2.start()
    elif(cameraId == 4):
        i2c = "i2cset -y 1 0x70 0x00 0x07"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, True)
        gp.output(12, False)
        time.sleep(0.5)
        picam2.start()
        print('On camera D')
    else:
        i2c = "i2cset -y 1 0x70 0x00 0x04"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)
        time.sleep(0.5)
        picam2.start()
        print('On camera A')

def generateFrames():
    while True:
        frame = picam2.capture_array()
        if frame is None:
            print("No frame captured")
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type:image/jpeg\r\n\r\n'+ frame + b'\r\n')

@app.route('/videofeed')
def videofeed():
    return Response(generateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/switchCamera', methods=['POST'])
def switch():
    cameraId = int(request.form.get('camera', 0))
    switchCamera(cameraId)

    return f"Switched to camera {cameraId}"

if __name__ == "__main__":
    #run app
    app.run(host = '0.0.0.0', port=5000, threaded = True, debug = False)
    picam2.close()    
