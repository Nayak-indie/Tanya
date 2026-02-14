import cv2
import time
from brain_py.memory.memory_core import MemoryCore

class VisionCore:
    def __init__(self, memory: MemoryCore, cam_index=0):
        self.cap = cv2.VideoCapture(cam_index)
        self.memory = memory

    def sense(self):
        ret, frame = self.cap.read()
        if not ret:
            return {"status": "offline"}

        observation = {
            "brightness": frame.mean(),
            "resolution": frame.shape[:2],
            "timestamp": time.time()
        }
        self.memory.remember("last_vision", observation)
        return observation

    def release(self):
        self.cap.release()
