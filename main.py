import os
from dotenv import load_dotenv
from src.extract_frames import FrameExtractor
from src.classify_frames import FrameClassifier
from src.report_generator import ReportGenerator


def main():
    load_dotenv()
    video_path = os.getenv('VIDEO_PATH')
    recognized_folder = os.getenv('RECOGNIZED_FOLDER')
    unrecognized_folder = os.getenv('UNRECOGNIZED_FOLDER')
    report_path = os.getenv('REPORT_PATH')

    os.makedirs(recognized_folder, exist_ok=True)
    os.makedirs(unrecognized_folder, exist_ok=True)

    # Extract frames  
    extractor = FrameExtractor(video_path)
    frames = extractor.extract_frames()

    # Classify frames
    classifier = FrameClassifier(recognized_folder, unrecognized_folder)
    report_data = classifier.classify_frames(frames)

    # Generate Report
    report_generator = ReportGenerator(report_path)
    report_generator.save_report(report_data)
    report_generator.print_summary()

if __name__ == "__main__":
    main()
