import warnings
warnings.filterwarnings("ignore")
import cv2
import re
import torch
import mouse as ms
import keyboard
import time
import numpy as np
from ultralytics import YOLO
import win32gui, win32ui, win32con

from ursina import *
from random import uniform
from ursina.prefabs.first_person_controller import FirstPersonController

window.title = "engine"

def make_walls(grid, scale=(10, 50, 10)):
	number_of_walls = 100

	walls = [None]*number_of_walls

	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if grid[i][j]:
				walls[i*10 + j] = Entity(model="cube", collider="box", position=(20*i - 100, 0, 20*j - 100), scale=scale, rotation=(0,0,0),
								texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))


class Human(Button):
	def __init__(self, x, y, z):
		super().__init__(
			parent=scene,
			model="assets/person_tom_1.obj",
			scale=1,
			position=(x,y,z),
			rotation=(0, 90, 0),
			collider="box"
		)

def input(key):
    # current drone position
    # boxcast data
    if key=="w":
        direction = Vec3(
            player.forward * (held_keys['w'] - held_keys['s'])
            + player.right * (held_keys['d'] - held_keys['a'])
            ).normalized()  
        
        hit_info = boxcast(player.position, thickness=(3,3), direction=direction, debug=False)
        player.camera_pivot.rotation_x = 20
    elif key == "r":
        player.rotation_y += 45
        player.camera_pivot.rotation_x = 20
    elif key == "l":
        player.rotation_y -= 45
        player.camera_pivot.rotation_x = 20
    
    



app = Ursina(size=(640,640), borderless=False, vsync=False)
Sky()
player = FirstPersonController(y=5, origin_y=-.5, gravity=0, speed=10)
player.mouse_sensitivity = Vec2(0,0)
ground = Entity(model='plane', scale=(170, 1, 170), color=color.lime, texture="white_cube",
				texture_scale=(100, 100), collider='box')

grid = [
	[0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
	[0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
	[0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
	[0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
	[0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
]

# walls, create them programmatically based on grid
make_walls(grid)

num = 100
humans=[None]*num
for i in range(num):
	sx=uniform(-50, 50)
	sy=uniform(-50, 50)
	sz=uniform(-50, 50)
	humans[i]=Human(sx, 0, sz)



class WindowCapture:
    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name=None):
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        border_pixels = 8
        titlebar_pixels = 40
        self.w = self.w - (border_pixels)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, 640,640)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (640,640), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (640, 640, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        img = img[...,:3]
        img = np.ascontiguousarray(img)
        return img

def draw_boxes(img, boxes, cls_dict):
    x = 0
    for box in boxes:
        xyxy = box.xyxy[0]
        cls = cls_dict[int(box.cls)]
        conf = round(box.conf.item(), 2)
        if cls == 'person' and conf>0.5 and int(xyxy[1]) >= 320:
            x += conf
            cv2.rectangle(img, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0,255,0), 2)
            cv2.putText(img, str(conf), (int(xyxy[0]), int(xyxy[1])-10), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255), 2)
    
    return x

def move_forward():
    keyboard.press('w')
    time.sleep(0.5)
    keyboard.release("w")

if __name__ == "__main__":
    model = YOLO("yolov8s.pt")
    cls_dict = model.names
    detect_matrix = np.zeros((17,17))
    done = False
    
    while not done:
        app.step()
        wincap = WindowCapture("ursina")
        frame = wincap.get_screenshot()
        frame = cv2.resize(frame, (640,640))
        frame = cv2.line(frame, (0,320), (640, 320), (0,0,255), 1)
        frame = cv2.line(frame, (0,320), (200,640), (0,0,255), 1)
        res = model(frame, verbose=False)
        boxes = res[0].boxes
        conf_sum = 0
        if boxes.shape[0]:
            conf_sum = draw_boxes(frame, boxes, cls_dict)

        curr_x = int(8 + player.position.x//10)
        curr_y = int(8 + player.position.z//10)
        if curr_x < 0 or curr_x > 16 or curr_y < 0 or curr_y > 16:
            done = True
        player_angle = (player.rotation_y + 360)%360
        if player_angle == 0:
            detect_matrix[curr_x][curr_y+1] = max(detect_matrix[curr_x][curr_y+1], conf_sum)
        if player_angle == 45:
            detect_matrix[curr_x-1][curr_y+1] = max(detect_matrix[curr_x-1][curr_y+1], conf_sum)
        if player_angle == 90:
            detect_matrix[curr_x-1][curr_y] = max(detect_matrix[curr_x-1][curr_y], conf_sum)
        if player_angle == 135:
            detect_matrix[curr_x-1][curr_y-1] = max(detect_matrix[curr_x-1][curr_y+1], conf_sum)
        if player_angle == 180:
            detect_matrix[curr_x][curr_y-1] = max(detect_matrix[curr_x][curr_y-1], conf_sum)
        if player_angle == 315:
            detect_matrix[curr_x+1][curr_y+1] = max(detect_matrix[curr_x+1][curr_y+1], conf_sum)
        if player_angle == 270:
            detect_matrix[curr_x+1][curr_y] = max(detect_matrix[curr_x+1][curr_y], conf_sum)
        if player_angle == 225:
            detect_matrix[curr_x+1][curr_y+1] = max(detect_matrix[curr_x+1][curr_y-1], conf_sum)
            
        print(detect_matrix.sum())
        cv2.imshow('window',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break