import numpy as np
import pyautogui
import cv2

class Eyes:
    def __init__(self):
        pass

    def find(self, pattern: np.array):
        screen = pyautogui.screenshot()
        gray = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(gray, pattern, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        score = result[max_loc[1]][max_loc[0]]
        if score >= 0.85:
            return max_loc
        else:
            return None
        