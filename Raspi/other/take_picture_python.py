#! /usr/bin/python

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
 
    # Save the image
    cv2.imwrite('01.jpg', image)

    # Wait for the user to press a key
    cv2.waitKey( 0 )

    # Disconnect from the robot
    bot.disconnect()
