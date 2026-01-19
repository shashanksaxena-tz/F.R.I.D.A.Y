import threading
import numpy as np

# Global State
lock = threading.Lock()
outputFrame = None
CURRENT_MODE = "normal"
drawing_canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
