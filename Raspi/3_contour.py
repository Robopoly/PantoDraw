#!/usr/bin/python

import numpy as np
import cv2
import cPickle

im = cv2.imread('1.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(im, contours, -1, (0,255,0), 3)
cv2.imshow('image',im)



width, height, depth = im.shape

image=np.zeros((width, height, 3),np.uint8) 
#image = im.copy()
cv2.drawContours(image, contours, -1, (0,255,0), 3)

cv2.imshow('WindowName',image) 

for c in contours:
    print c
    print '-------------------------'
    #index = []
    #for point in c:
    #    index.append(point)
    # Dump the keypoints
    #f = open("points.txt", "w")
    #f.write(cPickle.dumps(index))
    #f.write(c)
    #f.close()

print 'press any key to finish'

cv2.waitKey(0)

#cv2.destroyAllWindows()

