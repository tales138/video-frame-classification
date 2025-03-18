
import os
import torch
import cv2
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image

class FrameClassifier:
    def __init__(self, recognized_folder, unrecognized_folder):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.COCO_V1
        self.model = fasterrcnn_resnet50_fpn_v2(weights=self.weights).to(self.device)
        self.model.eval()
        self.preprocess = self.weights.transforms()
        self.recognized_folder = recognized_folder
        self.unrecognized_folder = unrecognized_folder

    def classify_frames(self, frames):
        detection_report = {
            "total_frames_processed": len(frames),
            "frames_recognized": 0,
            "frames_unrecognized": 0,
            "most_frequent_classes": {},
            "detection_details": []
        }

        for frame_count, frame in frames:
            img = torch.from_numpy(frame).permute(2, 0, 1)
            img_tensor = self.preprocess(img).unsqueeze(0).to(self.device)

            with torch.no_grad():
                prediction = self.model(img_tensor)[0]
                labels = [self.weights.meta["categories"][i] for i in prediction["labels"]]
                boxes = prediction["boxes"]
                scores = prediction["scores"]

                high_confidence_indices = [i for i, score in enumerate(scores) if score >= 0.7]
                boxes = boxes[high_confidence_indices]
                labels = [labels[i] for i in high_confidence_indices]
                scores = [scores[i].item() for i in high_confidence_indices]

                frame_data = {"frame": frame_count, "detections": []}

                if labels:
                    detection_report["frames_recognized"] += 1
                    for label in labels:
                        class_folder = os.path.join(self.recognized_folder, label)
                        os.makedirs(class_folder, exist_ok=True)

                    img_with_boxes = draw_bounding_boxes(img, boxes=boxes, labels=labels, colors="red", width=4)

                    for box, label, score in zip(boxes, labels, scores):
                        frame_data["detections"].append({"class": label, "confidence": round(score, 2)})
                        detection_report["most_frequent_classes"].setdefault(label, 0)
                        detection_report["most_frequent_classes"][label] += 1

                    im = to_pil_image(img_with_boxes.detach())
                    for label in labels:
                        im.save(f"{self.recognized_folder}/{label}/frame_{frame_count}.jpg")
                else:
                    detection_report["frames_unrecognized"] += 1
                    frame_data["detections"] = "No objects detected"
                    im = to_pil_image(img.detach())
                    im.save(f"{self.unrecognized_folder}/frame_{frame_count}.jpg")

                detection_report["detection_details"].append(frame_data)

        return detection_report

