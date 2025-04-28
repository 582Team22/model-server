"""
Author: Drew Meyer
File: app.py
Purpose: Module for a Flask app used to process a live
camera stream and compute object detection inference
"""

from flask import Flask, Response
import numpy as np
import os

# Set Torch Model Storage
os.environ['TORCH_HOME'] = os.path.join(os.path.dirname(__file__),'models')

import cv2
import torch

app = Flask(__name__)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# FIXES AN ISSUE WITH NUMPY, DONT ASK
def dummy_npwarn_decorator_factory():
    def npwarn_decorator(x):
        return x
    return npwarn_decorator
np._no_nep50_warning = getattr(np, '_no_nep50_warning', dummy_npwarn_decorator_factory)

def generate_frames():
    # Connect to RTMP stream
    cap = cv2.VideoCapture('rtmp://nginx-rtmp:1935/stream/drone_feed')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO Inference
        results = model(frame)

        for *xyxy, conf, cls in results.xyxy[0]:
            # Only draw if class is 'person' (class 0 in COCO dataset)
            if int(cls) == 0:
                cv2.rectangle(
                    frame,
                    (int(xyxy[0]), int(xyxy[1])),  # Top-left corner (x1, y1)
                    (int(xyxy[2]), int(xyxy[3])),  # Bottom-right corner (x2, y2)
                    (0, 255, 0),  # Color (Green)
                    2  # Thickness
                )

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream')
def stream():
    return "Streaming..."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
