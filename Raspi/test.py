#! /usr/bin/python

# This example shows the simplest way of getting an image from the raspi's camera. The image
# is an OpenCV image so we also show how to perform edge detection on the image

import numpy as np

import time
import argparse
import cv2
import py_websockets_bot

#---------------------------------------------------------------------------------------------------        
if __name__ == "__main__":

    # Set up a parser for command line arguments
    parser = argparse.ArgumentParser( "Gets an image from the raspi" )
    parser.add_argument( "hostname", default="localhost", nargs='?', help="The ip address of the remote robot" )

    args = parser.parse_args()
 
    # Connect to the robot
    bot = py_websockets_bot.WebsocketsBot( args.hostname )

    # Start streaming images from the camera
    bot.start_streaming_camera_images()

    # Get an image from the robot
    image, image_time = bot.get_latest_camera_image()

    # Display the image
    cv2.imshow( "Image", image )
 
    # Convert to grayscale
    gray_image = cv2.cvtColor( image, cv2.COLOR_RGB2GRAY )

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray_image[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)

    # Perform edge detection on the image
    edge_image = cv2.Canny( gray_image, threshold1=64, threshold2=192 )

    # Display the edge image
    cv2.imshow( "Edge Image", edge_image )

    # Wait for the user to press a key
    cv2.waitKey( 0 )

    # Disconnect from the robot
    bot.disconnect()
