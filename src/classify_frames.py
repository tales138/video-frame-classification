
import os
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2,FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image

class FrameClassifier:
    def __init__(self, recognized_folder, unrecognized_folder):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Set the device to GPU if available, otherwise use CPU
        self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.COCO_V1 # Load pre-trained weights for Faster R-CNN model with ResNet50 backbone
        self.model = fasterrcnn_resnet50_fpn_v2(weights=self.weights,box_score_thresh=0.7).to(self.device)# Initialize the Faster R-CNN model
        self.model.eval() # Set the model to evaluation mode (important for inference)
        self.preprocess = self.weights.transforms()# Define the image preprocessing pipeline using the weights' transforms
      
        # Set the paths for recognized and unrecognized folders

        self.recognized_folder = recognized_folder
        self.unrecognized_folder = unrecognized_folder

    def classify_frames(self, frames):
        # Initialize the detection report
        detection_report = {
            "total_frames_processed": len(frames),
            "frames_recognized": 0,
            "frames_unrecognized": 0,
            "most_frequent_classes": {},
            "detection_details": []
        }
        # Process each frame in the frames list
        for frame_count, frame in frames:
            img = torch.from_numpy(frame).permute(2, 0, 1)# Convert the frame to a tensor and move to correct dimensions for the model
            img_tensor = self.preprocess(img).unsqueeze(0).to(self.device)

            # Perform object detection using the model
            with torch.no_grad():
                prediction = self.model(img_tensor)[0]
                labels = [self.weights.meta["categories"][i] for i in prediction["labels"]] # Get predicted labels, bounding boxes, and scores
                boxes = prediction["boxes"]
                scores = prediction["scores"]

                high_confidence_indices = [i for i, score in enumerate(scores) if score >= 0.7]# Filter predictions based on a confidence threshold (0.7)
                boxes = boxes[high_confidence_indices]
                labels = [labels[i] for i in high_confidence_indices]
                scores = [scores[i].item() for i in high_confidence_indices]

                frame_data = {"frame": frame_count, "detections": []} # Initialize frame data for the current frame

                if labels:
                    detection_report["frames_recognized"] += 1

                    # Create folders for each detected class if not already present
                    for label in labels:
                        class_folder = os.path.join(self.recognized_folder, label)
                        os.makedirs(class_folder, exist_ok=True)

                    img_with_boxes = draw_bounding_boxes(img, boxes=boxes, labels=labels, colors="red", width=4)# Draw bounding boxes on the image


                    # Add detection details to frame data and count frequency of each class

                    for box, label, score in zip(boxes, labels, scores):
                        frame_data["detections"].append({"class": label, "confidence": round(score, 2)})
                        detection_report["most_frequent_classes"].setdefault(label, 0)
                        detection_report["most_frequent_classes"][label] += 1

                    im = to_pil_image(img_with_boxes.detach())# Convert the image with boxes to a PIL image and save it
                    for label in labels:
                        im.save(f"{self.recognized_folder}/{label}/frame_{frame_count}.jpg")
                else:
                    detection_report["frames_unrecognized"] += 1
                    frame_data["detections"] = "No objects detected"
                    im = to_pil_image(img.detach())
                    im.save(f"{self.unrecognized_folder}/frame_{frame_count}.jpg")

                detection_report["detection_details"].append(frame_data)# Add the current frame's detection data to the report

        return detection_report

