from detector.motion_detector import MotionDetector

if __name__ == "__main__":
    print("Starting Motion Detector...")
    detector = MotionDetector(video_source=0, min_area=800, save_clips=True)
    detector.process_stream()
