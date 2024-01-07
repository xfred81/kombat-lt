import pyautogui
import time


class Button:
    """Button on handset's GUI.
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
        try:
            r = pyautogui.locateCenterOnScreen(self._btn)
        except Exception:
            r = None
        return r

    def press(self):
        """Simulate usage of the button.
           Pointer will be moved over the button, and an event will simulate a press on the mouse's left button for
           step._press_step_time, and then released.
        """
        try:
            pyautogui.moveTo(self.pos)
            pyautogui.mouseDown()
            time.sleep(self._press_step_time)
            self._press_total_time += self._press_step_time
            pyautogui.mouseUp()
        except Exception:
            pass
        
    def cancel(self):
        self._press_total_time = 0

    def learn_press(self, dx: int, dy: int):
        """Declare a new movement implied by the button.
        
        To be used after the press() method above;
        This "averages" movement and compute a more accurate "expected motion"
        when a button is pressed.

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
    """A virtual handset.
    """
    def __init__(self, name: str, path: str, button_filenames: list):
        self._buttons = []
        self._name = name
        for i in button_filenames:
            self._buttons.append(Button(f"{path}/{i}.png"))

    @property
    def name(self) -> str:
        """Get the name of the handset.

        Returns:
            str: Name (as KStars Control)
        """
        return self._name

    def is_valid(self) -> bool:
        """Test if handset is initialized.

        Returns:
            bool: True if all buttons have been detected.
        """
        for b in self._buttons:
            if b.pos is None:
                return False

        return True

    def get_button(self, idx: int) -> Button:
        """Return the indicated button.

        Args:
            idx (int): Index of the desired button

        Returns:
            Button: result is a Button object
        """
        return self._buttons[idx]

    def get_buttons_number(self) -> int:
        """Return the number of buttons. 

        Returns:
            int: Number of buttons on the handset.
        """
        return len(self._buttons)
