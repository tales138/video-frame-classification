import json

class ReportGenerator:
    def __init__(self, report_path):
        self.report_path = report_path


    #save report
    def save_report(self, report_data):
        with open(self.report_path, "w") as f:
            json.dump(report_data, f, indent=4)
            
    #print summary in terminal after running the application
    def print_summary(self):
        with open(self.report_path, "r") as f:
            report_data = json.load(f)

        print(f"Total Frames Processed: {report_data['total_frames_processed']}")
        print(f"Recognized Frames: {report_data['frames_recognized']}")
        print(f"Unrecognized Frames: {report_data['frames_unrecognized']}")
        print(f"Most Frequent Classes: {report_data['most_frequent_classes']}")
        print(f"Report saved at {self.report_path}")
