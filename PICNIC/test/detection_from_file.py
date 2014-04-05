# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 20:08:58 2014

@author: sim
"""

import cv
import os

HAAR_PATH = "/usr/local/share/OpenCV/haarcascades/"

imcolor = cv.LoadImage('face.jpg') # input image
# loading the classifiers
haarFace = cv.Load(os.path.join(HAAR_PATH, 'haarcascade_frontalface_default.xml'))
haarEyes = cv.Load(os.path.join(HAAR_PATH, 'haarcascade_eye.xml'))
# running the classifiers
storage = cv.CreateMemStorage()
detectedFace = cv.HaarDetectObjects(imcolor, haarFace, storage)
detectedEyes = cv.HaarDetectObjects(imcolor, haarEyes, storage)

# draw a green rectangle where the face is detected
if detectedFace:
 for face in detectedFace:
  cv.Rectangle(imcolor,(face[0][0],face[0][1]),
               (face[0][0]+face[0][2],face[0][1]+face[0][3]),
               cv.RGB(155, 255, 25),2)

# draw a purple rectangle where the eye is detected
if detectedEyes:
 for face in detectedEyes:
  cv.Rectangle(imcolor,(face[0][0],face[0][1]),
               (face[0][0]+face[0][2],face[0][1]+face[0][3]),
               cv.RGB(155, 55, 200),2)

cv.NamedWindow('Face Detection', cv.CV_WINDOW_AUTOSIZE)
cv.ShowImage('Face Detection', imcolor)
cv.WaitKey()