"""
Motion Detection using OpenCV

This program uses some code from: http://www.steinm.com/blog/motion-detection-webcam-python-opencv-differential-images/
"""

import smtplib
import io
import datetime
import socket
import cv2
import threading
import time
import os
import sys
import re

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

###### Threading ######
def input_thread(user_input_ref):
    while user_input_ref[0] != 'q':
        user_input_ref[0] = raw_input("Enter 'q' to exit: ")
###### Threading ######

######  EMAIL ######
def send_mail(mail_attr, group_num):

  RECEIVE_EMAIL = mail_attr[0]
  EMAIL = mail_attr[1]
  PASSWORD = mail_attr[2]
  RECEIVE_TEXT = mail_attr[3]
  PHONE_NUM = mail_attr[4]
  CARRIER = mail_attr[5]

  MAILBOX = None

  if CARRIER == 'at&t':
    MAILBOX = '@mms.att.net'
  elif CARRIER == 't-mobile':
    MAILBOX = '@tmomail.net'
  elif CARRIER == 'verizon':
    MAILBOX = '@vzwpix.com'
  elif CARRIER == 'sprint':
    MAILBOX = '@pm.sprint.com'

  print("Sending message...")
  smtp = smtplib.SMTP()
  smtp.connect('smtp.gmail.com', 587)
  smtp.starttls()
  smtp.login(EMAIL, PASSWORD)

  from_addr = socket.gethostname() + " <motion@detection.com>"
  to_addr = EMAIL

  subj = "Motion Detection Alert"
  date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )

  message_text = ("ALERT!\n\nMotion has been detected on: " 
               + socket.gethostname() + "\n")
  mime_msg = MIMEText(message_text, 'plain')

  msg = MIMEMultipart()
  msg["From"] = from_addr
  msg["To"] = EMAIL
  msg["Subject"] = subj
  msg.attach(mime_msg)

  path = './Pictures/Group_' + group_num + '/'

  imageCount = 0
  for currPath, dirs, files in os.walk(path):
    for filename in files:
      # Walk through the files and 
      # let MIMEImage guess the file type
      fullPath = os.path.join(currPath, filename)
      with open(fullPath, 'rb') as fp:
        img = MIMEImage(fp.read())
        fp.close()
        imageCount += 1
        img.add_header('Content-Disposition', 'attachment; filename="image_' 
                       + str(imageCount) + '.png"')
        msg.attach(img)
  if RECEIVE_EMAIL == True:
    smtp.sendmail(from_addr, to_addr, msg.as_string())
  if RECEIVE_TEXT == True:
    to_addr = str(PHONE_NUM) + MAILBOX
    msg["To"] = to_addr
    smtp.sendmail(from_addr, to_addr, msg.as_string())

  smtp.quit()
  print("Message sent!")
######  EMAIL ######

######  Image Differences ######
def diffImg(t0, t1):
    d2 = cv2.absdiff(t1, t0)
    return d2
######  Image Differences ######

######  MAIN  ######
def main(argv):
    
    cap = cv2.VideoCapture(0)

    # Check for camera
    
    if not cap.isOpened():
      print("No camera detected")
      exit(1)

    BRIGHTNESS = None
    THRESH = None
    RECEIVE_EMAIL = None
    EMAIL_ADDR = None
    PASSWORD = None
    RECEIVE_TEXT = None
    PHONE_NUM = None
    CARRIER = None

    # Read security.conf file and set constants
    try:
      fp = open(argv[1])
      for lineCounter, line in enumerate(fp):
        lineCounter += 1
        if lineCounter == 1:
          BRIGHTNESS = float(re.split(': ', line)[1])
        elif lineCounter == 2:
          THRESH = float(re.split(': ', line)[1])
        elif lineCounter == 3:
          string = re.split(': ', line)[1].lower().strip()
          if string == 'y':
            RECEIVE_EMAIL = True
          else:
            RECEIVE_EMAIL = False
        elif lineCounter == 4:
          if RECEIVE_EMAIL == True:
            EMAIL_ADDR = re.split(': ', line)[1].lower()
        elif lineCounter == 5:
          if RECEIVE_EMAIL == True:
            PASSWORD = re.split(': ', line)[1].strip()
        elif lineCounter == 6:
          string = re.split(': ', line)[1].lower().strip()
          if string == 'y':
            RECEIVE_TEXT = True
          else:
            RECEIVE_TEXT = False
        elif lineCounter == 7:
          if RECEIVE_TEXT == True:
            PHONE_NUM = int(re.split(': ', line)[1])
        elif lineCounter == 8:
          if RECEIVE_TEXT == True:
            CARRIER = re.split(': ', line)[1].lower().strip()
    except:
      print("\nsecurity.conf file is corrupted, run ./configure.sh -r for a reset")
      exit(1)

    mail_attr = [RECEIVE_EMAIL, EMAIL_ADDR, PASSWORD, 
                 RECEIVE_TEXT, PHONE_NUM, CARRIER]

    cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, BRIGHTNESS/255.0)

    blurVar   = 3
    THRESH    = 60 # 20-low, 60 default, 120-high
    minPixels = 10

    vidDirName  = './Video'
    vidPath     = ''
    picDirName  = './Pictures'
    picPath     = ''
    vidCount    = 0
    picCount    = 0
    startVid    = False
    endVid      = False
    groupCount  = 1

    if not os.path.exists(picDirName):
      os.mkdir(picDirName)
    if not os.path.exists(vidDirName):
      os.mkdir(vidDirName)

    while(groupCount < 51):
      picPath = os.path.join(picDirName, 'Group_' + str(groupCount))
      if not os.path.exists(picPath):
        os.mkdir(picPath)
        vidPath = os.path.join(vidDirName, 'Group_' + str(groupCount))
        if not os.path.exists(vidPath):        
          os.mkdir(vidPath)
        break
      else:
        groupCount += 1

    FPS = 15
    cap.set(cv2.cv.CV_CAP_PROP_FPS, FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    out = cv2.VideoWriter(os.path.join(vidPath, 
                                       str(time.strftime("%Y_%m_%d")) + 
                                       '-output.avi'),
                          fourcc, FPS, (640,480))

    user_input = [None]
    myThread = threading.Thread(target=input_thread, args=(user_input,))
    myThread.daemon = True
    myThread.start()

    # Read two images first:
    prev_frame = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
    prev_frame = cv2.flip(prev_frame, 1)
    prev_frame = cv2.blur(prev_frame,(blurVar,blurVar))
    curr_frame = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
    curr_frame = cv2.flip(curr_frame, 1)
    curr_frame = cv2.blur(curr_frame,(blurVar,blurVar))

    vidTime = 0
    vidTimeCounter = 0

    startTime   = time.time()
    currentTime = 0
    counterTime = 0
    seconds     = 0
    secondCounter = 0
    count       = 0

    MAX_TIMER = 2
    timer     = 0

    print("\nCountdown until camera activation (in seconds)")
    while(timer < MAX_TIMER):
      ret, frame = cap.read()
      if ret==True:
        frame = cv2.flip(frame, 1)

        prev_frame = curr_frame       
        curr_frame = cv2.blur(frame,(blurVar,blurVar))
        curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)
        currentTime = time.time()
        timer = currentTime - startTime
        secondCounter = currentTime - counterTime
        if 1 < secondCounter: 
          counterTime = time.time()
          print(MAX_TIMER - int(timer))

    startTime = time.time()
    currentTime = 0

    x = 0
    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret==True:
        frame = cv2.flip(frame, 1)
        prev_frame = curr_frame
        curr_frame = cv2.blur(frame,(blurVar,blurVar))
        curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)

        motionFrame = diffImg(prev_frame, curr_frame)

        ret, motionFrame = cv2.threshold(motionFrame,THRESH,255,cv2.THRESH_BINARY)

        currentTime = time.time()
        seconds = currentTime - startTime
        secondCounter = currentTime - counterTime

        # Checks for movement every second
        if cv2.countNonZero(motionFrame) > minPixels:
          if 1 < secondCounter:
            counterTime = time.time()
            if endVid == False:
              startVid = True
            count += 1
            print("movement detected " + str(count))
            
            if 99 < count:
              count = 0


        if(startVid == True):
          out.write(frame)
          currentTime = time.time()
          vidTime = currentTime - vidTimeCounter
          if 1 < vidTime:
            vidTimeCounter = time.time()
            vidCount += 1
            picCount += 1
          if picCount < 11 and picCount % 2 == 0:
            # Save frame to file
            cv2.imwrite(os.path.join(picPath, 
                                     str(time.strftime("%Y_%m_%d")) + 
                                     '-(' + str(picCount/2) + ').png'),
                        frame)
          if 10 < vidCount:
            print('Max time reached')
            vidCount = 0
            picCount = 0
            startVid = False
            endVid   = True
            break
        if user_input[0] == 'q':
          break
      else:
        break

    if RECEIVE_EMAIL == True or RECEIVE_TEXT == True:
      send_mail(mail_attr, str(groupCount))

    # Release everything if job is finished
    cap.release()
    out.release()
    myThread.join()
    exit(0)
######  MAIN  ######

if __name__ == "__main__":
    main(sys.argv)
