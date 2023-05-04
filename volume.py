#installing important libraries
import cv2
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import sys
import math
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
from ctypes import POINTER, pointer,cast
from comtypes import CLSCTX_ALL
import numpy as np

#volume control library usage
devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface, POINTER(IAudioEndpointVolume))

#Getting volume range using volume.GetVolumeRange() method
volRange=volume.GetVolumeRange()
minVol, maxVol, volBar, volPer=volRange[0], volRange[1], 400, 0

#setting frame for webcam
w_cam, h_cam = 640,480
############

cap=cv2.VideoCapture(0)
cap.set(3,w_cam)
cap.set(4,h_cam)

handob=HandDetector(detectionCon=0.7,minTrackCon=0.6)

while True:
    success, img = cap.read()
    #img = cv2.flip(img,1)
    hand,img = handob.findHands(img)
    #print(hand)
    #print(success)

    if(len(hand)==1):
        hand1=hand[0]
        lmList=hand1['lmList']
        fingers=handob.fingersUp(hand1)
        #finger is a list that shows which finger are up ad whch are not
        #0 = thumb 4= little finger and when a finger is up it gives 1
        #print(fingers[1])
        if(fingers[0] and fingers[1]):#therefore when finger[0](thumb) and figers[1](index) are up then only it will get executed
            f1x,f1y=lmList[4][0],lmList[4][1]
            #print("Finger x-coordinate of f1 is", f1x1)
            #print("Finger y-coordinate of f1 is", f1y1)
            f2x,f2y=lmList[8][0],lmList[8][1]
            cv2.circle(img,(f1x,f1y),10,(0,255,0),cv2.FILLED)
            cv2.circle(img,(f2x,f2y),10,(0,255,0),cv2.FILLED)
            cv2.line(img,(f1x,f1y),(f2x,f2y),(255,255,0),3)
            cx,cy= (f1x+f2x) //2 , (f1y+f2y)//2
            cv2.circle(img,(cx,cy),12,(51,153,255),cv2.FILLED)
            lent=math.hypot((f2x-f1x),(f2y-f1y))
            #print(l)
            # if(l<=25):
            #     print("hello")


            # Converting Length range into Volume range using numpy.interp()
            vol = np.interp(lent, [50, 150], [minVol, maxVol])

            # Changing System Volume using volume.SetMasterVolumeLevel() method
            volume.SetMasterVolumeLevel(vol, None)
            volBar = np.interp(lent, [50, 150], [400, 150])
            volPer = np.interp(lent, [50, 150], [0, 100])


            # Drawing Volume Bar using cv2.rectangle() method
            cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,1, (0, 0, 0), 3)
        

    cv2.imshow('sarwagya', img)
    if(cv2.waitKey(1)==ord('q')):
        print("Exit")
        sys.exit(0)
    elif cv2.waitKey(1)==ord('Q'):
        print("Exit")
        sys.exit(0)
    
    #cv2.waitKey(1)
    """[{'lmList': [[636, 452], [606, 465], [573, 466], [555, 472], [531, 480], [560, 388], [538, 345], [530, 316], [523, 287], [597, 357], [583, 296], [571, 262], [562, 232], [630, 342], [620, 283], [608, 242], [598, 207], [659, 340], [654, 290], [648, 253], [642, 221]], 'bbox': (523, 207, 136, 273), 'center': (591, 343), 'type': 'Left'}, {'lmList': [[162, 493], [223, 467], [274, 419], [317, 388], [358, 370], [240, 309], [269, 241], [295, 207], [321, 177], [211, 300], [233, 217], [257, 167], [280, 125], [179, 307], [194, 225], [215, 174], [236, 131], [143, 328], [146, 262], [157, 216], [169, 174]], 'bbox': (143, 125, 215, 368), 'center': (250, 309), 'type': 'Right'}]"""