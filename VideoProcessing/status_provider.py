#!/usr/bin/env python3
import cv2
import sys
import numpy as np
import socket
import time

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
MODEL_PROTO     = 'models/ssd_mobilenet_v1_coco.pbtxt'
MODEL_WEIGHTS   = 'models/frozen_inference_graph.pb'
PERSON_CLASS_ID = 1       # COCO class ID for "person"
CONF_THRESHOLD  = 0.5
HOST            = '127.0.0.1'
PORT            = 50007
LOOP_PERIOD     = 0.0001   # seconds per detection loop (1.0 → 1 Hz)

# ──────────────────────────────────────────────────────────────────────────────
# 1) Load the DNN
# ──────────────────────────────────────────────────────────────────────────────
net = cv2.dnn.readNetFromTensorflow(MODEL_WEIGHTS, MODEL_PROTO)

# ──────────────────────────────────────────────────────────────────────────────
# 2) TCP server setup
# ──────────────────────────────────────────────────────────────────────────────
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind((HOST, PORT))
server_sock.listen(1)
print(f"[INFO] Waiting for LabVIEW on {HOST}:{PORT} …")
conn, addr = server_sock.accept()
print(f"[INFO] LabVIEW connected from {addr}")

# ──────────────────────────────────────────────────────────────────────────────
# 3) Helper functions
# ──────────────────────────────────────────────────────────────────────────────
def send_pause():
    """Send PAUSE over TCP."""
    try:
        conn.sendall(b"PAUSE\n")
        print("[TIMER] PAUSE")
    except BrokenPipeError:
        print("[ERROR] Connection lost when sending PAUSE")
        sys.exit(1)

def send_resume():
    """Send RESUME over TCP."""
    try:
        conn.sendall(b"RESUME\n")
        print("[TIMER] RESUME")
    except BrokenPipeError:
        print("[ERROR] Connection lost when sending RESUME")
        sys.exit(1)

# ──────────────────────────────────────────────────────────────────────────────
# 4) Main detection loop
# ──────────────────────────────────────────────────────────────────────────────
def detect_pedestrians(stream_source=0):
    cap = cv2.VideoCapture(stream_source)
    if not cap.isOpened():
        sys.exit(f"[ERROR] Could not open video stream: {stream_source}")

    while True:
        t0 = time.time()
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Frame grab failed—exiting.")
            break

        # Run the network
        blob = cv2.dnn.blobFromImage(frame, size=(300,300), swapRB=True, crop=False)
        net.setInput(blob)
        detections = net.forward()

        # Count persons
        h, w = frame.shape[:2]
        person_count = 0
        for i in range(detections.shape[2]):
            score = float(detections[0,0,i,2])
            cls   = int(detections[0,0,i,1])
            if cls == PERSON_CLASS_ID and score > CONF_THRESHOLD:
                person_count += 1
                box = detections[0,0,i,3:7] * np.array([w,h,w,h])
                x1,y1,x2,y2 = box.astype(int)
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

        # Send PAUSE or RESUME every loop
        if person_count == 0:
            send_pause()
        else:
            send_resume()

        # Overlay and show
        cv2.putText(frame, f"Pedestrians: {person_count}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.imshow('Pedestrian Detection (DNN)', frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Maintain desired loop period
        elapsed = time.time() - t0
        to_sleep = max(0.0, LOOP_PERIOD - elapsed)
        time.sleep(to_sleep)

    # Cleanup
    cap.release()
    conn.close()
    server_sock.close()
    cv2.destroyAllWindows()
    print("[INFO] Clean shutdown.")

# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    detect_pedestrians(stream_source=0)