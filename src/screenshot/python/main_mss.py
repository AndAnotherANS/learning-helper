
import mss
from PIL import Image, ImageGrab
import pyautogui

import cv2 as cv
import numpy as np
import time

w, h = pyautogui.size()
print("PIL Screen Capture Speed Test")
print("Screen Resolution: " + str(w) + 'x' + str(h))
from PIL import Image, ImageGrab 
    
# creating an image object 

tempScreen = ImageGrab.grab((0,0,w,h))

monitor = (0,0,w,h)
img = None
n_frames = 1
i=0
with mss.mss() as sct:
    while True:
        t0 = time.time()
        
        img = sct.grab(monitor)
        print(time.time()-t0)
        img = np.array(img)                         # Convert to NumPy array
        
        small = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
        cv.imshow("Computer Vision", small)

        # Break loop and end test
        key = cv.waitKey(1)
        if key == ord('q'):
            break
        
        elapsed_time = time.time() - t0
        avg_fps = (n_frames / elapsed_time)
        print("Average FPS: " + str(avg_fps))
        n_frames += 1
        i+=1
        if(i>0): 
            break