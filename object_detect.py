#source: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2


#capture the video file
b="blood.mp4"
c="Center.avi"
d="Deformed.avi"
i="Inlet.avi"
videofile=c
vs = cv2.VideoCapture(videofile)

#width = vs.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
#height = vs.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
width = vs.get(3)
height=vs.get(4)
print("Width x: ",width, " Height y: ",height)
print("Frame Number,x coordinate of ROI,Weidth,Height,Width/Height")

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
j=0
totalframesampled=0
totalcelldetected=0
while True:
    
    j+=1
    if j%1000 !=0 :
        continue
    totalframesampled+=1
	# grab the current frame and initialize the occupied/unoccupied
	# text
    frame = vs.read()
    frame = frame[1]
    text = "Unoccupied"
 
	# if the frame could not be grabbed, then we have reached the end
	# of the video
    if frame is None:
        break
        
	
 
	# resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	# if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
        
	
	
	

		# compute the absolute difference between the current frame and
	# first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	    cv2.CHAIN_APPROX_SIMPLE)
	#print(cnts)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    #print("Frame: ",j)
    #print(cnts)
 
	# loop over the contours
    for c in cnts:
        #print("c:",c)
        area=cv2.contourArea(c)
        #print("Area:",area)
        minarea=250
        if area<=minarea:
            continue
        
        
        
        (x, y, w, h) = cv2.boundingRect(c)# top left x,y, wid,hei
        condition_center_inlet=x>440 and x<450
        condition_deformation=y>240 and y<300
        if condition_center_inlet:
            totalcelldetected+=1
            print("totalcelldetected:",totalcelldetected)
            print(j,x,y,w,h,w/h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"
            k=0
            frameskip=10 # for center and inlet skip=10
            while k<frameskip:
                k+=1
                temp=vs.read()
            break
	
	
		# if the contour is too small, ignore it
	
	    
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
	
	
			# draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
	    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
	    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
 
	
    
        
	
 
# cleanup the camera and close any open windows
vs.release()
cv2.destroyAllWindows()
print("Total frame: ",j-1)
print("Frame sampled: ",totalframesampled)
print("Total object detected: ",totalcelldetected)
