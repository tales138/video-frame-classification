from dotenv import load_dotenv
import os
load_dotenv()
FRAME_RATE = int(os.getenv('FRAME_RATE'))
class FrameExtractor:
    def __init__(self, video_path, frame_rate=FRAME_RATE):
        self.video_path = video_path
        self.frame_rate = frame_rate

    def extract_frames(self):
        import cv2
        # Open the video using OpenCV
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames in the video
        
        frames = []
        for frame_count in range(0, total_frames, int(fps * self.frame_rate)):  # Iterate over frames with the desired frame rate
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)  # Set the position to the specific frame
            ret, frame = cap.read()  # Read the frame at that position
            if not ret:
                break
            frames.append((frame_count, frame))  # Store the frame
        
        cap.release()
        return frames