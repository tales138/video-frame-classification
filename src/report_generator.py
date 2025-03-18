import json

class ReportGenerator:
    def __init__(self, report_path):
        self.report_path = report_path

    def save_report(self, report_data):
        with open(self.report_path, "w") as f:
            json.dump(report_data, f, indent=4)

    def print_summary(self):
        with open(self.report_path, "r") as f:
            report_data = json.load(f)

        print(f"Total de frames processados: {report_data['total_frames_processed']}")
        print(f"Frames reconhecidos: {report_data['frames_recognized']}")
        print(f"Frames não reconhecidos: {report_data['frames_unrecognized']}")
        print(f"Classes mais frequentes reconhecidas: {report_data['most_frequent_classes']}")
        print(f"Relatório salvo em {self.report_path}")
