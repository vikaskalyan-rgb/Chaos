import cv2
import numpy as np
import copy
import math
import pyautogui
import time

cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 20  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0

isBgCaptured = 0   # bool, whether the background captured
triggerSwitch = False  # if true, keyborad simulator works

pyautogui.FAILSAFE = False
SCREEN_X, SCREEN_Y = pyautogui.size()
CLICK = MOVEMENT_START = None

mouseX,mouseY = 1.3,1.3


def gesture_function(used_defect,count_defects,frame):
	#print("gesture")
	global MOVEMENT_START,CLICK
	if used_defect is not None:
		best = used_defect
		if count_defects == 1:
			x = best['x']
			y = best['y']
			display_x = x
			display_y = y
			#print(display_x,display_y)
			if MOVEMENT_START is not None:
				M_START = (x, y)
				x = x - MOVEMENT_START[0]
				y = y - MOVEMENT_START[1]
				x = x * (SCREEN_X / CAMERA_X)
				y = y * (SCREEN_Y / CAMERA_Y)
				MOVEMENT_START = M_START
				print("X: " + str(x) + " Y: " + str(y))
				pyautogui.moveRel(x, y)
			else:
				MOVEMENT_START = (x, y)

			cv2.circle(frame, (display_x, display_y), 5, [255, 255, 255], 20)
		elif count_defects == 2 and CLICK is None:
		    CLICK = time.time()
		    pyautogui.click()
		elif count_defects == 3 and CLICK is None:
		    CLICK = time.time()
		    pyautogui.rightClick()
		else:
		    MOVEMENT_START = None

		if CLICK is not None:
		    if CLICK < time.time():
		         CLICK = None
def printThreshold(thr):
    print("! Changed threshold to "+str(thr))


def removeBG(frame):
    fgmask = bgModel.apply(frame,learningRate=learningRate)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


def calculateFingers(res,drawing):
    used_defect = None
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 1:
        defects = cv2.convexityDefects(res, hull)
        if type(defects) != type(None):

            cnt = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) 
                if angle <= math.pi / 2:
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
                if cnt == 1 and angle <= 90:
                	used_defect = {"x": start[0], "y": start[1]}
            return True, cnt,used_defect
    return False, 0,used_defect

camera = cv2.VideoCapture(0)
camera.set(10,200)
cv2.namedWindow('trackbar')
cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)


while camera.isOpened():
    ret, frame = camera.read()
    CAMERA_X, CAMERA_Y, channels = frame.shape
    threshold = cv2.getTrackbarPos('trh1', 'trackbar')
    frame = cv2.bilateralFilter(frame, 5, 50, 100)
    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                 (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
    cv2.imshow('original', frame)

    if isBgCaptured == 1:
        img = removeBG(frame)
        img = img[0:int(cap_region_y_end * frame.shape[0]),int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]
        #cv2.imshow('mask', img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        #cv2.imshow('blur', blur)
        ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        #cv2.imshow('ori', thresh)


        thresh1 = copy.deepcopy(thresh)
        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1
        if length > 0:
            for i in range(length):
                temp = contours[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i

            res = contours[ci]
            hull = cv2.convexHull(res)
            drawing = np.zeros(img.shape, np.uint8)
            cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

            isFinishCal,cnt,used_defect = calculateFingers(res,drawing)
            print(cnt)
            if triggerSwitch is True:
                if isFinishCal is True:
                	gesture_function(used_defect,cnt,frame)


        cv2.imshow('output', drawing)

    k = cv2.waitKey(10)
    if k == 27: 
        camera.release()
        cv2.destroyAllWindows()
        break
    elif k == ord('b'): 
        bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
        isBgCaptured = 1
        print( '!!!Background Captured!!!')
    elif k == ord('r'):
        bgModel = None
        triggerSwitch = False
        isBgCaptured = 0
        print ('!!!Reset BackGround!!!')
    elif k == ord('n'):
        triggerSwitch = True
        print ('!!!Trigger On!!!')
