import RPi.GPIO  as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
print("Distance Measurement In Progress")
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT)

GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

print("Waiting For Sensor To Settle")

time.sleep(2)
GPIO.output(TRIG, True)

time.sleep(0.00001)

GPIO.output(TRIG, False)
while GPIO.input(ECHO)==0:
  pulse_start=time.time()
while GPIO.input(ECHO)==1:

  pulse_end = time.time()    
pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150
distance = round(distance, 2)


if distance < 10:
   db=1
else:
   db=0;
print(db)

if db=1:
    import cv2
    import imutils
    import numpy as np
    import pytesseract
    from PIL import Image
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(640, 480))
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("s"):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grey scale
            gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
            edged = cv2.Canny(gray, 30, 200) #Perform Edge detection
            cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,              cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
            screenCnt = None
            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                if len(approx) == 4:
                    screenCnt = approx
                    break
                if screenCnt is None:
                   detected = 0
                   print ("No contour detected")
                else:
                    detected = 1
                    if detected == 1:
                        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
                        mask = np.zeros(gray.shape,np.uint8)
                        new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
                        new_image = cv2.bitwise_and(image,image,mask=mask)
                       (x, y) = np.where(mask == 255)
                       (topx, topy) = (np.min(x), np.min(y))
                       (bottomx, bottomy) = (np.max(x), np.max(y))
                       Cropped = gray[topx:bottomx+1, topy:bottomy+1]
                       text = pytesseract.image_to_string(Cropped, config='--psm 11')
                       print("Detected Number is:",text)
                       file=open('car.txt','a')
                       file.write('/n')
                       file.write(text)
                       file.close()

                       cv2.imshow("Frame", image)
                       cv2.imshow('Cropped',Cropped)
                       cv2.waitKey(0)
                       break
    cv2.destroyAllWindows()
else:
    pass


GPIO.cleanup()