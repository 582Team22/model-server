# 🚀 Real-Time Object Detection Server

This project implements a fully containerized real-time object detection system deployed on AWS EC2 with GPU acceleration.  
It uses Docker Compose to orchestrate an nginx-rtmp streaming server and a Flask-based YOLOv5 inference server.


## 📸 Live Demo

- OBS streams video to the RTMP server
- YOLOv5 detects objects on each frame using GPU inference
- Flask server streams processed frames back to the browser

Example access:
Stream to: `rtmp://<EC2-IP>:1935/stream`
Stream key:` drone_feed`
View detections: `http://<EC2-IP>:5001/video_feed`


## 📦 Architecture

```plaintext
[OBS/Webcam] --> [nginx-rtmp server] --> [Flask YOLOv5 Inference] --> [Web Browser Stream]
```
- nginx-rtmp: Ingests live RTMP video stream
- Flask App: Pulls frames from RTMP, runs YOLOv5 inference, outputs processed frames
- Docker: Manages containers with GPU support (NVIDIA runtime)


## 🛠️ Technologies Used
- AWS EC2 g4dn.xlarge (Tesla T4 GPU)
- Docker with NVIDIA Container Toolkit
- nginx-rtmp for RTMP streaming
- Flask + OpenCV for server-side inference
- YOLOv5s w/ COCO weights
- OBS Studio for video input
- Python 3.10


## 🚀 Setup Instructions
1. Clone the repository
  ```
  git clone git@github.com:582Team22/model-server.git
  cd model-server
  ```

2. Configure the environment
Make sure you have:
- NVIDIA drivers installed
- Docker and NVIDIA Container Toolkit installed
- EC2 security groups allowing ports:
   - `1935` (RTMP input)
   - `5001` (Flask web server)

3. Build and start the services
```
docker compose build --no-cache
docker compose up -d
```
- Use `-d` to run containers detached in the background

4. Stream video from OBS
In OBS Settings:
 - Server: `rtmp://<your-ec2-ip>:1935/stream`
 - Stream Key: `drone_feed`
Start streaming.

5. View detections
Open your browser:
`http://<your-ec2-ip>:5001/video_feed`
Watch real-time object detections rendered with bounding boxes.


## 📋 Project Structure
```plaintext
streaming-ml-server/
│
├── app/
│   ├── app.py           # Flask server for YOLOv5 inference
│   ├── Dockerfile       # Flask app container
│   ├── requirements.txt # Python dependencies
│   └── yolov5s.pt          # YOLOv5s weights (downloaded automatically)
│
├── docker-compose.yml    # Orchestration of nginx-rtmp + Flask containers
└── README.md             # Project documentation
```
