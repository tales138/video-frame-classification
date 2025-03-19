
FROM python:3.13.2


WORKDIR /video-frame-detection


RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install opencv-python
RUN pip install python-dotenv

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]