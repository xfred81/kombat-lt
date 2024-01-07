import pyautogui
import time

class Button:
    """Button on handset's GUI
    """
    def __init__(self, btn: str):
        self._btn = btn
        self._press_total_time = 0
        self._press_step_time = 0.1 # s
        # self._delay = 2

        self._data = []

        self._dxdy_per_unit = None

    @property
    def pos(self) -> tuple:
        """Get position of button on the screen

        Returns: x, y coordinates (or None)
        """
        return pyautogui.locateCenterOnScreen(self._btn)

    def press(self):
        pyautogui.moveTo(self.pos)
        pyautogui.mouseDown()
        time.sleep(self._press_step_time)
        self._press_total_time += self._press_step_time
        pyautogui.mouseUp()

    def add_delta(self, dx: int, dy: int):
        """Declare a new movement implied by the button.
        
        This allows to "average" movement and compute a more accurate "expection motion"
        when a particular button is pressed.

        Args:
            dx (int): apparent movement on x-axis
            dy (int): apparent movement on y-axis
        """
        self._data.append([self._press_total_time, dx, dy])
        self._press_total_time = 0
        self._data = self._data[:5]

        dx = 0
        dy = 0
        for i in self._data:
            dx += i[1]/i[0]
            dy += i[2]/i[0]

        l = len(self._data)/self._press_step_time
        dx /= l
        dy /= l
        self._dxdy_per_unit = dx, dy

    @property
    def expected_motion(self) -> tuple:
        """Get movement to expect if button is used

        Returns:
            tuple: predicted dx, dy moves
        """
        return self._dxdy_per_unit


class Handset:
    def __init__(self, path: str, button_filenames: list):
        self._buttons = []
        for i in button_filenames:
            self._buttons.append(Button(f"{path}/{i}.png"))

    def is_valid(self):
        for b in self._buttons:
            if b.pos is None:
                return False

        return True

    def get_button(self, idx: int) -> Button:
        return self._buttons[idx]
    
    def get_buttons_number(self):
        return len(self._buttons)

class HandsetKS:
    def __init__(self):
        self._buttons = []
        self._pattern = None
        self._pattern_p0 = None
    
        self._pattern = cv2.cvtColor(np.array(clipboard), cv2.COLOR_RGB2GRAY)

        for i in ['up', 'down', 'left', 'right']:
            self._buttons.append(Button(f'{i}.png'))
        
    def _find_pattern(self):
        screen = pyautogui.screenshot()
        gray = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(gray, self._pattern, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        score = result[max_loc[1]][max_loc[0]]
        if score >= 0.85:
            return max_loc
    
    def _measure_press_delta(self, b: int):
        btn = self._buttons[b]
        p0 = self._find_pattern()
        self._press(btn)
        time.sleep(2)
        p1 = self._find_pattern()
        if p0 is not None and p1 is not None:
            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]
            btn.add_delta(dx, dy)
            return dx, dy
        else:
            return None
        
    def learn(self):
        self._pattern_p0 = self._find_pattern()
        for b in range(0, len(self._buttons)):
            m = None
            while m is None:
                m = self._measure_press_delta(b)
        
    @staticmethod    
    def _delta(v0, v1):
        dx = v1[0] - v0[0]
        dy = v1[1] - v0[1]
        return dx, dy, math.sqrt(dx**2+dy**2)
    
    def adjust_now(self):
        p1 = None
        
        while p1 is None:
            p1 = self._find_pattern()
     
        dx, dy, dt = self._delta(self._pattern_p0, p1)   
        
        if dt > 10:     
            min_ndt = None
            min_ndt_b = None
            for b in range(0, len(self._buttons)):
                btn = self._buttons[b]
                xp = btn.expected_motion
            
                ndx = dx + xp[0]
                ndy = dy + xp[1]
            
                ndt = math.sqrt(ndx**2 + ndy**2)
                if min_ndt is None or ndt < min_ndt:
                    min_ndt = ndt
                    min_ndt_b = b
            
            if min_ndt < dt:
                self._measure_press_delta(min_ndt_b)
            else:                
                time.sleep(1)
        return dt