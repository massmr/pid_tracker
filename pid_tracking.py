# Import necessary packages
from multiprocessing import Manager, Process
from imutils.video import VideoStream
from classes.objCenter import ObjCenter
from classes.pid import PID
#import board
#import busio
import RPi.GPIO as GPIO
#from adafruit_pca9685 import PCA9685
from PCA9685 import PCA9685
import argparse
import signal
import time
import sys
import cv2
import subprocess
import numpy as np

# Define the range for the motors
# PWM is ranged [0, 4095] : 600 = 180°
#SERVO_MIN = 150
#SERVO_MAX = 600

# Function to handle keyboard interrupt
def signal_handler(sig, frame):
    # Print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")
    # Exit
    sys.exit()

# Function to use libcamera-still self-stream without tcp in order to increase velocity
def capture_frame(interval=0.2):
    cmd = "libcamera-still -o - --width 640 --height 480 --timeout 1"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    frame = np.frombuffer(result.stdout, dtype=np.uint8)
    return cv2.imdecode(frame, cv2.IMREAD_COLOR)

def obj_center(args, objX, objY, centerX, centerY):
    # Signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the videostream
    # For PiCamera v2
    #vs = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
    
    # For TCP video stream
    #vs = cv2.VideoCapture("tcp://localhost:8554")
    #if not vs.isOpened():
    #    print("[ERROR] Unable to open video stream.")
    #    sys.exit(1)
    #vs.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # For self webcam
    #vs = VideoStream(src=0).start()
    
    # pre-heat picamera V2
    time.sleep(2.0)

    # Initialize the object center finder
    obj = ObjCenter(args["cascade"])
    
    # Loop indefinitely
    while True:
        # Grab the frame from the threaded video stream and flip it
        # vertically (since our camera was upside down)
        
        # If using piCameraV2
        #ret, frame = vs.read()
        
        # For video stream
        frame = capture_frame()
        frame = cv2.flip(frame, 1)
        
        # Calculate the center of the frame as this is where we will
        # try to keep the object
        (H, W) = frame.shape[:2]
        centerX.value = W // 2
        centerY.value = H // 2
        
        # Find the object's location
        objectLoc = obj.update(frame, (centerX.value, centerY.value))
        ((objX.value, objY.value), rect) = objectLoc
        
        # Extract the bounding box and draw it
        if rect is not None:
            (x, y, w, h) = rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Display the frame to the screen
        cv2.imshow("Pan-Tilt Face Tracking", frame)
        cv2.waitKey(1)

def pid_process(output, p, i, d, objCoord, centerCoord):
    # Signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create a PID and initialize it
    p = PID(p.value, i.value, d.value)
    p.initialize()
    
    # Loop indefinitely
    while True:
        # Calculate the error
        error = centerCoord.value - objCoord.value
        # Update the value
        output.value = p.update(error)

def in_range(val, start, end):
    # Determine the input value is in the supplied range
    return (val >= start and val <= end)

def set_servo_pan(angle):
    pwm.setRotationAngle(1, angle)

def set_servo_tilt(angle):
    pwm.setRotationAngle(0, angle)

def set_servos(pan, tlt):
    # Signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    
    # Init servos
    servoRange = (0, 180)
    pwm = PCA9685()

    try:
        pwm.setPWMFreq(50)

        while True:
            if in_range(pan.value, servoRange[0], servoRange[1]):
                set_servo_pan(pan.value)
            if in_range(tlt.value, servoRange[0], servoRange[1]):
                set_servo_tilt(tlt.value)
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        pwm.deinit()
        print("[INFO] PCA9685 PWM stopped")


# Check to see if this is the main body of execution
if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", type=str, required=True,
                    help="path to input Haar cascade for face detection")
    args = vars(ap.parse_args())

    # Start a manager for managing process-safe variables
    with Manager() as manager:
        
        # Set integer values for the object center (x, y)-coordinates
        centerX = manager.Value("i", 0)
        centerY = manager.Value("i", 0)
        
        # Set integer values for the object's (x, y)-coordinates
        objX = manager.Value("i", 0)
        objY = manager.Value("i", 0)
        
        # Pan and tilt values will be managed by independent PIDs
        pan = manager.Value("i", 0)
        tlt = manager.Value("i", 0)
        
        # Set PID values for panning
        panP = manager.Value("f", 0.09)
        panI = manager.Value("f", 0.08)
        panD = manager.Value("f", 0.002)
        
        # Set PID values for tilting
        tiltP = manager.Value("f", 0.11)
        tiltI = manager.Value("f", 0.10)
        tiltD = manager.Value("f", 0.002)

        # We have 4 independent processes
        # 1. objectCenter  - finds/localizes the object
        # 2. panning       - PID control loop determines panning angle
        # 3. tilting       - PID control loop determines tilting angle
        # 4. setServos     - drives the servos to proper angles based
        #                    on PID feedback to keep object in center
        
        processObjectCenter = Process(target=obj_center,
                                       args=(args, objX, objY, centerX, centerY))
        processPanning = Process(target=pid_process,
                                  args=(pan, panP, panI, panD, objX, centerX))
        processTilting = Process(target=pid_process,
                                  args=(tlt, tiltP, tiltI, tiltD, objY, centerY))
        processSetServos = Process(target=set_servos, args=(pan, tlt))
        
        # Start all 4 processes
        processObjectCenter.start()
        processPanning.start()
        processTilting.start()
        processSetServos.start()
        
        # Join all 4 processes
        processObjectCenter.join()
        processPanning.join()
        processTilting.join()
        processSetServos.join()
