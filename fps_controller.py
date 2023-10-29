import keyboard
import time
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



time.sleep(3)


move_forward()
turn(left=True)
move_forward(4)
turn()
move_forward()

# take_screenshot()