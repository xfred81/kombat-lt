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
            dx += i[1]/(i[0]/self._press_step_time)
            dy += i[2]/(i[0]/self._press_step_time)

        l = len(self._data)
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
    def __init__(self, name: str, path: str, button_filenames: list):
        self._buttons = []
        self._name = name
        for i in button_filenames:
            self._buttons.append(Button(f"{path}/{i}.png"))
            
    @property
    def name(self):
        return self._name

    def is_valid(self):
        for b in self._buttons:
            if b.pos is None:
                return False

        return True

    def get_button(self, idx: int) -> Button:
        return self._buttons[idx]
    
    def get_buttons_number(self):
        return len(self._buttons)
