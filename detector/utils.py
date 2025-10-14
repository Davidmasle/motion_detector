import cv2
import os
from datetime import datetime

def save_motion_clip(frames, output_dir="output/"):
    if not frames:
        return
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}{timestamp}.mp4"

    height, width, _ = frames[0].shape
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), 20, (width, height))

    for frame in frames:
        out.write(frame)
    out.release()
    print(f"[INFO] Saved motion clip: {filename}")
