import warnings
warnings.filterwarnings("ignore")
import cv2
import numpy as np
import torch
from ultralytics import YOLO
import win32gui, win32ui, win32con, win32api
import numpy as np
import win32gui, win32ui, win32con


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

        print(window_rect)

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
    for box in boxes:
        xyxy = box.xyxy[0]
        cls = cls_dict[int(box.cls)]
        conf = round(box.conf.item(), 2)
        if cls=='person' and conf>0.5:
            cv2.rectangle(img, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0,255,0), 2)
            cv2.putText(img, str(conf), (int(xyxy[0]), int(xyxy[1])-10), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255), 2)


if __name__ == "__main__":
    model = YOLO("yolov8s.pt")
    wincap = WindowCapture("ursina")
    cls_dict = model.names
    while True:
        frame = wincap.get_screenshot()
        frame = cv2.resize(frame, (640,640))
        res = model(frame, verbose=False)
        boxes = res[0].boxes
        if boxes.shape[0]:
            draw_boxes(frame, boxes, cls_dict)
        cv2.imshow('window',frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break