import numpy as np
import cv2
from mss import mss
from PIL import Image
import time
import torch
import keyboard
import mouse
from PIL import ImageGrab

def move_forward(duration=3):
    keyboard.press('w')
    time.sleep(duration)
    keyboard.release("w")

def turn(left=False, duration=0.5):
    if left:        
        mouse.drag(0, 0, 100, 0, absolute=False, duration=duration)
    else:
        mouse.drag(0, 0, -100, 0, absolute=False, duration=duration)

def take_screenshot():
    # 2560 x 1440
    ss_region = (0, 0, 2560, 1440)
    ss_img = ImageGrab.grab(ss_region)
    print(ss_img.getdata())
    ss_img.save(r"C:\Users\SWC\Desktop\DL-Project-main\DL-Project-main\SS3.jpg")





bounding_box = {'top': 0, 'left': 0, 'width': 2560, 'height': 1440 }

sct = mss()
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
# im = 'https://ultralytics.com/images/zidane.jpg'

# Inference
# results = model(im)

# results.show()

while True:
    time.sleep(5)
    sct_img = sct.grab(bounding_box)
    # cv2.imshow('screen', np.array(sct_img))
    result = model(np.array(sct_img))
    result.show()
    # PASS RESULT TO ALGO
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
