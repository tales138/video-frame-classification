# video-frame-classification
This project extracts frames from a video and uses the pytoech pre-trained fasterrcnn_resnet50_fpn_v2 to perform image classification and detection on them. 


Project Strucuture
```
VIDEO-FRAME-CLASSIFICATION/
│── output/
│   ├── recognized_frames/
│   ├── unrecognized_frames/
│   ├── .gitkeep
│── reports/
│── src/
│   ├── __init__.py
│   ├── classify_frames.py
│   ├── extract_frames.py
│   ├── report_generator.py
│── .env
│── .gitignore
│── docker-compose.yaml
│── dockerfile
│── main.py
│── README.md
│── requirements.txt
│── video.mp4

```

# CONFIG VARIABLES

In the .env file, it is possible to config the necessary varibles to run the application

```
VIDEO_PATH = "video.mp4"
RECOGNIZED_FOLDER = "output/recognized_frames"
UNRECOGNIZED_FOLDER = "output/unrecognized_frames"
REPORT_PATH = "reports/detection_report.json"
FRAME_RATE = 1
```

# Running the repository

**Note: This application it was developed to support NVIIDIA CUDA hardware accelaration. CUDA 12.8 was used. If you want to run it using this feature check your CUDA version. If you prefer this application the can also be executed using only the CPU.

In the requitements.txt there is the pytorch used in this application.

## Executing on Docker
clone this repository and execute the follwoing docker commands inside the repository directory.

```
docker compose build
```

```
docker compose up
```

## Executing using a PYTHON enviroment.

run the following commands:

```
python -m venv video-frame-classification
```

```
video-frame-classification\Scripts\activate

```
```
pip install  -r requirements.txt 

```
```
python main.py
```

## Executing wihtout  a PYTHON enviroment.

run the following commands:

```
pip install  -r requirements.txt 

```
```
python main.py

```

# Files description

The main.py file executes the applicationm

Inside the src folder, there are three files : 

- classify_frames.py responsible for running object classification and detection

- extract_frames.py responsible for extracting the frames from the demo video.

- report_genrator.py responsible for helping to generate the detection_report.json file.


** The detection_report.json file has the following informations:**

```
"total_frames_processed": 
"frames_recognized": 
"frames_unrecognized": 
"most_frequent_classes": 
"most_frequent_classes":{
    "frame": 
    {
        "class":
        "confidence":
        }
}
```

## NOTE:
In the env file it is possible to change video path. It is important ot highlight that a demo video is provided in this repository for testing the application.

# REQUIREMENTS

```
python version used 3.13.2

```

```
--pre
torch
torchvision
torchaudio
--index-url https://download.pytorch.org/whl/nightly/cu128
numpy==2.1.2
opencv-python==4.11.0.86
python-dotenv==1.0.1

```