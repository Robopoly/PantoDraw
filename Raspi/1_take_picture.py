#! /usr/bin/python

import os
import cv2

while(True):

    ##Take image with Raspberry Pi camera
    # Way faster if we take the picture using raspistill than python !!!
    os.system("raspistill -o 1.jpg")

    im = cv2.imread('./1.jpg')

    # Display the resulting frame
    cv2.imshow('image',im)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()


