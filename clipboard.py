from PIL import ImageGrab, Image
import numpy as np
import time
import cv2


class Clipboard:
    """
    Query clipboard
    """
    def __init__(self):
        clipboard = None
        print("Waiting for the pattern to track in clipboard... ", end='', flush=True)
        while not isinstance(clipboard, Image.Image):
            try:
                clipboard = ImageGrab.grabclipboard()
            except Exception:
                pass
            time.sleep(1)

        self._contents = cv2.cvtColor(np.array(clipboard), cv2.COLOR_RGB2GRAY)
        print("ok")
        
    def as_grayscale(self) -> np.array:
        """Get clipboard as a grayscale image

        Returns:
            cv2.Image: contents of clipboard, as a grayscale OpenCV image
        """
        return self._contents
