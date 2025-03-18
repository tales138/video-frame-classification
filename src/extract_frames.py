

class FrameExtractor:
    def __init__(self, video_path, frame_rate=1):
        self.video_path = video_path
        self.frame_rate = frame_rate

    def extract_frames(self):
        import cv2
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = 0
        frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % int(fps * self.frame_rate) == 0:
                frames.append((frame_count, frame))

            frame_count += 1

        cap.release()
        return frames
