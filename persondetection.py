from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import threading
import argparse
import keyboard
import imutils
import cv2
import firebase_admin
# import firebase
from firebase_admin import credentials
# from firebase_admin import credentials, initialize_app, storage
from firebase_admin import db
import datetime, time
import os
from pynput.keyboard import Key, Listener
from imageSending import imageSend
# Fetch the service account key JSON file contents
cred = credentials.Certificate('fingerprintdoorlock-8bb72-firebase-adminsdk-6328x-e02a42aad0.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {'databaseURL': 'https://fingerprintdoorlock-8bb72.firebaseio.com/'})

if os.path.exists("images") is False:
    os.mkdir("images")
fldr_template = "data/img{}"
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



def sketch_transform(image):
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)


    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 3)
    if rects.any():
        print('ok')
        notify = db.reference("/intrusion")
        x = datetime.datetime.now()
        timestr = time.strftime("%Y%m%d-%H%M")
        cv2.imwrite('images/img{0}.jpg'.format(timestr) , image)
        t2=threading.Thread(target=imageSend,args=('images/img{0}.jpg'.format(timestr),))
        t2.start()
        t2.join()
        notify.update({'values': str(x.strftime("%H:%M , %b %d,%Y"))})
        # cv2.imwrite(os.path.join('detected','%d.jpg' % str(x.strftime(("%H:%M , %b %d,%Y"))),image))
        # time.sleep(15)

    else:
        print('no')

    return image

cap = cv2.VideoCapture('1.mp4')

def ROI():

    while True:
        global r
        ret,im0 = cap.read()
        im0 = imutils.resize(im0, width=900)
        showCrosshair = False
        fromCenter = False
        r = cv2.selectROIs("Image", im0, showCrosshair, fromCenter)
        if (len(r)==0):
            cv2.putText(im0, 'Please select Region of interest', (10,500), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255), 2)
            print('Select intrusion')
        else:
            break

def Pedestrien(cap):
    while True:
        image_frame = cap
        for i in range(0, len(r)):
            cv2.rectangle(image_frame, (r[i][0], r[i][1]), (r[i][0] + r[i][2], r[i][1] + r[i][3]), (0, 0, 255), 3)
            rect_img = image_frame[r[i][1]:r[i][1] + r[i][3], r[i][0]:r[i][0] + r[i][2]]
            sketcher_rect = rect_img
            sketcher_rect = sketch_transform(sketcher_rect)
            image_frame[r[i][1]:r[i][1] + r[i][3], r[i][0]:r[i][0] + r[i][2]] = sketcher_rect

        return image_frame