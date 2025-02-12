import RPi.GPIO as gp
import os
import time
import cv2
from picamera2 import Picamera2
from flask import Flask, Response, request, jsonify
from threading import Lock
from flask_cors import CORS

#gpio setup
gp.setwarnings(False)
gp.setmode(gp.BOARD)
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)
print('GPIO setup complete')

#picamera setup
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main = {"size": (640, 480), "format": "BGR888"}, buffer_count=6))

#set register for arducam camera
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

#lock for camera when switching
camera_lock = Lock()

#variable for keeping track of camera
currentCamera = 1

app = Flask(__name__)
CORS(app)

#func for switching cameras
def switchCamera(cameraId):
    #select global camera and current camera
    global picam2
    global currentCamera
    with camera_lock:
        #close old one and start new one
        picam2.close()
        picam2 = Picamera2()
        picam2.configure(picam2.create_video_configuration(main = {"size": (640, 480), "format": "BGR888"}, buffer_count=6))

        print('camera id: ' + str(cameraId))

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
            currentCamera = 1
        elif(cameraId == 2):
            i2c = "i2cset -y 1 0x70 0x00 0x05"
            os.system(i2c)
            gp.output(7, True)
            gp.output(11, False)
            gp.output(12, True)
            time.sleep(0.5)
            picam2.start()
            print('On camera B')
            currentCamera = 2
        elif(cameraId == 3):
            print('On camera C')
            i2c = "i2cset -y 1 0x70 0x00 0x06"
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, True)
            gp.output(12, False)
            time.sleep(0.5)
            picam2.start()
            currentCamera = 3
        elif(cameraId == 4):
            i2c = "i2cset -y 1 0x70 0x00 0x07"
            os.system(i2c)
            gp.output(7, True)
            gp.output(11, True)
            gp.output(12, False)
            time.sleep(0.5)
            picam2.start()
            print('On camera D')
            currentCamera = 4
        else:
            i2c = "i2cset -y 1 0x70 0x00 0x04"
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, False)
            gp.output(12, True)
            time.sleep(0.5)
            picam2.start()
            print('On camera A')
            currentCamera = 1

#generates and shows video feed
def generateFrames():
    while True:
        frame = picam2.capture_array()
        if frame is None:
            print("No frame captured")
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame'
               b'Content-Type:image/jpeg\r\n\r\n'+ frame + b'\r\n')



#route for adjusting how the videofeed is shown
@app.route('/')
def index():
    return '''
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 0;
                background: black;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
            }
            img {
                width: 100vw;
                height: 100vh;
                object-fit: cover;
            }
        </style>
    </head>
    <body>
        <img src="/videoFeed" />
    </body>
    </html>
    '''

# route for showing the videofeed
@app.route('/videoFeed')
def videofeed():
    return Response(generateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# route for camera switch post requests
@app.route('/switchCamera', methods=['POST'])
def switch():
    #get global currentcamera
    global currentCamera
    
    #handle request
    data = request.get_json()
    if data and 'camera' in data:
        cameraDirect = data['camera']
    else:
        cameraDirect = '1'

    print(f'camera direction: {cameraDirect}')
    
    #select camera to be show
    if(cameraDirect == "next"):
        if (currentCamera <= 3):
            currentCamera += 1
        else:
            currentCamera = 1
    elif(cameraDirect == "prev"):
        if (currentCamera >=2):
            currentCamera -= 1
        else:
            currentCamera = 4

    #call switch camera
    switchCamera(currentCamera)

    return jsonify({"message": f"Switched to camera {currentCamera}"})

if __name__ == "__main__":
    #run app
    app.run(host = '0.0.0.0', port=5000, threaded = True, debug = False)
    picam2.close()    
