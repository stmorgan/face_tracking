import cv2 
import time
import os
import numpy as np
from adafruit_servokit import ServoKit


# Detect all faces in current image. 
def detect_face(img):
    coords = face_cascade.detectMultiScale(img, 1.3, 5)
    # for (x,y,w,h) in coord:
        # cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,255),5)
    return coords

def move_camera(coord, img, pan, tilt):
    deadband = 10
    new_pan = pan 
    new_tilt = tilt 
    
    if len(coord) != 0:  # if faces detected
        x = coord[0]
        y = coord[1]
        w = coord[2] 
        h = coord[3]

        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),5)  # Box around face
    
        print(coord)
    
        # Pan 
        pan_center = x + w/2  # Horizontal centre of the box in pixels. 
        pan_angle = pan_center*0.28125
        if abs(pan_angle - pan) > deadband: 
            new_pan = int(pan + 0.15*(pan_angle - pan))
        else: 
            cv2.putText(img, "Naughty or Nice?", (50, 440), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)
        print("pan, pan_angle,new_pan : ", pan, pan_angle, new_pan)
        new_pan = max(0, new_pan)
        new_pan = min(180, new_pan)
        kit.servo[0].angle = new_pan
    
        # Tilt
        tilt_center = y + h/2  # Vertial centre of the box in pixels. 
        tilt_angle = -tilt_center*0.375 + 180 # Tilt angle of center of box. 
        if abs(tilt_angle - tilt) > deadband: 
            new_tilt = int(tilt + 0.15*(tilt_angle - tilt))
        print("tilt, tilt_angle, new_tilt, : ", tilt, tilt_angle, new_tilt)
 
        new_tilt = max(0, new_tilt)
        new_tilt = min(180, new_tilt)
    
        # print("pan, tilt", new_pan, new_tilt)
        # cv2.circle(img, (int(pan_center), int(tilt_center)), 5, (0,0,255), -1) # Mark centre of box. 
    
        print("box centre (px): ", pan_center, tilt_center)
        print("box centre (deg): ", pan_angle, tilt_angle)
        kit.servo[1].angle = new_tilt
    
    return new_pan, new_tilt
    
def get_biggest_face(coords): # Return size and coordinates of largest (closest) detected face. 
    sizes = []
    coord = []

    # Get sizes
    for coord in coords: 
        w = coord[2]
        h = coord[3]
        size = w*h 
        sizes.append(size)
        # print(coord, size)

    if len(coord) != 0: # if faces detected
        print("Not empty: ", sizes)
        max_index = sizes.index(max(sizes))
        coord = coords[max_index]  
    else: coord =[] # no faces found
    
    
    return coord
    
def draw_box(coord, image):
    x = coord[0]
    y = coord[1]
    w = coord[2] 
    h = coord[3]
    
    cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0),5)
    
    return

def get_color_gray_images():
    (ret, oimage) = cam.read()
    color_image = cv2.resize(oimage, (640,480))
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    return color_image, gray_image

######################
# Start Main Program #
######################    

# Set up servo instance
kit = ServoKit(channels=16)

# Set up camera connection
cam = cv2.VideoCapture(0)

# Load the cascade
face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')

pan = 90
tilt = 90
kit.servo[0].angle = pan
kit.servo[1].angle = tilt
time.sleep(2)

while True:
    # os.system('clear')
    color_image, gray_image = get_color_gray_images()   # Get images, gray version too.
    coords = detect_face(gray_image)
    coord = get_biggest_face(coords)
    (pan,tilt) = move_camera(coord, color_image, pan, tilt)
    cv2.imshow('Preview', color_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
