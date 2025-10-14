import cv2
import time
import logging
from datetime import datetime
from .utils import save_motion_clip

class MotionDetector:
    def __init__(self, video_source=0, min_area=500, save_clips=True):
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            logging.error(f"Cannot open video source {video_source}")
            raise ValueError(f"Cannot open video source {video_source}")

        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
        self.min_area = min_area
        self.save_clips = save_clips
        self.is_recording = False
        self.frame_buffer = []
        self.last_motion_time = 0

        logging.basicConfig(
            filename='logs/events.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
        )

    def process_stream(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fgmask = self.fgbg.apply(gray)
            fgmask = cv2.medianBlur(fgmask, 5)

            contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            motion_detected = False

            for c in contours:
                if cv2.contourArea(c) < self.min_area:
                    continue
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion_detected = True

            if motion_detected:
                now = datetime.now()
                logging.info(f"Movement detected at {now.strftime('%H:%M:%S')}")
                self.last_motion_time = time.time()

                if self.save_clips:
                    self.frame_buffer.append(frame.copy())
                    if not self.is_recording:
                        self.is_recording = True
            else:
                if self.is_recording and time.time() - self.last_motion_time > 2:
                    save_motion_clip(self.frame_buffer)
                    self.frame_buffer = []
                    self.is_recording = False

        self.cap.release()
