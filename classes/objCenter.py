# import necessary packages
import imutils
import cv2

class ObjCenter:
    def __init__(self, haarPath):
        # load OpenCV's Haar cascade face detector
        self.detector = cv2.CascadeClassifier(haarPath)
    

    def update(self, frame, frameCenter):
        # Convert frames to grey shades to boost process
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect all faces inside the frame
        rects = self.detector.detectMultiScale(gray, scaleFactor=1.05,
            minNeighbors=9, minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)
        
        # Check if faces were found
        if len(rects) >= 1:
            # Init largest face (assumption : largest face is also the closest one)
            largest_face = None
            largest_area = 0
            
            # Iteration over each faces
            for (x, y, w, h) in rects:
                # Print closest face dimensions
                print(f"Detected face at ({x}, {y}), width: {w}, height: {h}")

                # Calculate area of face box
                area = w * h
                
                # Compare each aeras with current largest area
                if area > largest_area:
                    largest_area = area
                    largest_face = (x, y, w, h)

            # Extract and return center of largest face
            if largest_face is not None:
                (x, y, w, h) = largest_face
                faceX = int(x + (w / 2.0))
                faceY = int(y + (h / 2.0))
                return ((faceX, faceY), largest_face)

        # If no face detected, return center of frame in order to maintain
        # camera stable
        return (frameCenter, None)
