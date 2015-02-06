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
    #bot = py_websockets_bot.WebsocketsBot( args.hostname )
        
    #res = cv2.waitKey(0)
    #print 'You pressed %d (0x%x), LSB: %d (%s)' % (res, res, res % 256, repr(chr(res%256)) if res%256 < 128 else '?')

    #cv2.destroyAllWindows()

    print 'Ready !'
    print 'Press INTRO to take the picture'

    cv2.waitKey( 10 )
    print 'checkpoint'
    cv2.waitKey( 0 )

    # Connect to the robot
    bot = py_websockets_bot.WebsocketsBot( args.hostname )

    print 'starting the camera...'	
    # Start streaming images from the camera
    bot.start_streaming_camera_images()

    print 'getting an image...'
    # Get an image from the robot
    image, image_time = bot.get_latest_camera_image()

    # Display the image
    cv2.imshow( "Image", image )

    cv2.waitKey( 0 )
 
    # Save the image
    print 'Saving the image...'
    cv2.imwrite('01.jpg', image)

    # Wait for the user to press a key
    cv2.waitKey( 0 )

    print 'End of the program'
    # Disconnect from the robot
    bot.disconnect()
