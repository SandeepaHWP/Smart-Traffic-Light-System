import cv2
import numpy as np

# Replace IP address with the one from your IP Webcam app
cap = cv2.VideoCapture("http://192.168.129.44:8080/video")

min_width_react = 80  
min_height_react = 80

offset = 6
counter = 0
detect = []

algo = cv2.createBackgroundSubtractorKNN(detectShadows=False)

def center_handle(x, y, w, h):
    x1 = int(x + w / 2)
    y1 = int(y + h / 2)
    return x1, y1

while True:
    ret, frame1 = cap.read()
    if not ret:
        print("Failed to grab frame from IP Webcam.")
        break

    frame_height = frame1.shape[0]
    frame_width = frame1.shape[1]

    count_line_position = frame_height - 50  # Horizontal line near bottom

    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = algo.apply(blur)

    dilated = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    morphed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    morphed = cv2.morphologyEx(morphed, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(morphed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw horizontal half-line
    cv2.line(frame1, (0, count_line_position), (frame_width // 2, count_line_position), (255, 127, 0), 3)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if w >= min_width_react and h >= min_height_react:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center = center_handle(x, y, w, h)
            detect.append(center)
            cv2.circle(frame1, center, 4, (0, 0, 255), -1)

    for (cx, cy) in detect:
        if (count_line_position - offset) < cy < (count_line_position + offset):
            if cx < frame_width // 2:  # Ensure it's in the left half
                counter += 1
                detect.remove((cx, cy))
                print("Vehicle Counter:", counter)

    cv2.putText(frame1, "Vehicle Counter: " + str(counter), (50, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    cv2.imshow('IP Webcam Vehicle Detection', frame1)

    if cv2.waitKey(1) == 13:
        break

cap.release()
cv2.destroyAllWindows()
