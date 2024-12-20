# Import necessary packages
from multiprocessing import Manager, Process
from imutils.video import VideoStream
from classes.objCenter import ObjCenter
from classes.pid import PID
from classes.PiCamera2VideoStream import VideoStream
import RPi.GPIO as GPIO
from PCA9685 import PCA9685
import argparse
import signal
import time
import sys
import cv2
import subprocess
import numpy as np
import os

# Virtual VNC server
#os.environ['DISPLAY'] = ':1'

# Define the range for the motors
pwm = PCA9685()
servoRangeX = (10, 170)
servoRangeZ = (0, 80)

# Function to handle keyboard interrupt
def signal_handler(sig, frame):
    # Print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")
    # Turn off servos
    for channel in range(16):
        PCA9685.setPWM(channel, 0, 0)
    # Exit
    sys.exit()

def obj_center(args, objX, objY, centerX, centerY):
    # Signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    # Initialize the VideoStream with a lower resolution and limited FPS
    vs = VideoStream(resolution=(620, 480), framerate=24)
    # Pre-heat the camera
    time.sleep(2.0)
    # Initialize the object center finder
    obj = ObjCenter(args["cascade"])
    # Loop indefinitely
    while True:
        # For video stream
        frame  = vs.read()
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

def pid_process(isPan, output, p, i, d, objCoord, centerCoord):
    # Signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    # Create a PID and initialize it
    p = PID(p.value, i.value, d.value)
    p.initialize()
    # Loop indefinitely
    while True:
        # Calculate the error
        error = centerCoord.value - objCoord.value
        # Update the value - Angles are reversed
        if isPan:
            output.value = -(p.update(error)) + 90
            print(f"value: {output.value}")
        else: 
            output.value = -(p.update(error)) + 60
            print(f"value: {output.value}")

def in_range(val, start, end):
    # Determine the input value is in the supplied range
    print(f"start: {start} end: {end} | val: {val} ")
    if val >= start and val <= end:
        return val
    else:
        print(f"[DEBUG] val is out of range: {val}")
        return 0

def set_servos(pan, tlt):

    # Signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    
    # Init servos
    pwm.setPWMFreq(50)
    try:
        # Check range and set servos
        while True:
            # Set servoX - PAN
            if in_range(pan.value, servoRangeX[0], servoRangeX[1]):
                pwm.setRotationAngle(1, pan.value)
                time.sleep(0.1)
            # Set servoZ - TILT
            if in_range(tlt.value, servoRangeZ[0], servoRangeZ[1]):
                pwm.setRotationAngle(0, tlt.value)
                time.sleep(0.1)
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        print("[INFO] PCA9685 PWM stopped")


# Check to see if this is the main body of execution
if __name__ == "__main__":
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", type=str, required=True,
                    help="path to input Haar cascade for face detection")
    args = vars(ap.parse_args())
    
    # Pre init camera position
    pwm.setRotationAngle(1, 90)
    pwm.setRotationAngle(0, 60)
    time.sleep(0.1)

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
        panP = manager.Value("f", 0.03)
        panI = manager.Value("f", 0.0002)
        panD = manager.Value("f", 0.0015)
        
        # Set PID values for tilting
        tiltP = manager.Value("f", 0.03)
        tiltI = manager.Value("f", 0.00015)
        tiltD = manager.Value("f", 0.0005)

        # We have 4 independent processes
        # 1. objectCenter  - finds/localizes the object
        # 2. panning       - PID control loop determines panning angle
        # 3. tilting       - PID control loop determines tilting angle
        # 4. setServos     - drives the servos to proper angles based
        #                    on PID feedback to keep object in center
        
        processObjectCenter = Process(target=obj_center,
                                       args=(args, objX, objY, centerX, centerY))
        processPanning = Process(target=pid_process,
                                  args=(True, pan, panP, panI, panD, objX, centerX))
        processTilting = Process(target=pid_process,
                                  args=(False, tlt, tiltP, tiltI, tiltD, objY, centerY))
        processSetServos = Process(target=set_servos, args=(pan, tlt))
        
        # Start all 4 processes
        print("Starting processObjectCenter...")
        processObjectCenter.start()
        time.sleep(0.1)
        print("Starting processPanning...")
        processPanning.start()
        time.sleep(0.1)
        print("Starting processTilting...")
        processTilting.start()
        time.sleep(0.1)
        print("Starting set_servos process...")
        processSetServos.start()
        time.sleep(0.1)
        
        # Join all 4 processes
        processObjectCenter.join()
        processPanning.join()
        processTilting.join()
        processSetServos.join()
