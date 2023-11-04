import keyboard
import time
import mouse

def move_forward(duration=3):
    keyboard.press('w')
    time.sleep(duration)
    keyboard.release("w")


def turn(left=False, duration=0.5):
    if left:        
        mouse.drag(0, 0, 95, 0, absolute=False, duration=duration)
    else:
        mouse.drag(0, 0, -100, 0, absolute=False, duration=duration)

time.sleep(5)

# move_forward()
turn(left=True)
# move_forward(4)
# turn()
# move_forward()
# take_screenshot()