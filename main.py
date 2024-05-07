from ultralytics import YOLO
import cv2
import requests, time
import math
from picamera2 import Picamera2

# start webcam
picam2 = Picamera2()
picam2.start()

# model
model = YOLO("./models/cat-v3-430-imgs.pt")

# object classes
classNames = ["cats"]

target_url = "http://localhost:8000/set"

while True:
    success, img = picam2.capture_array()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
            # "cats"가 감지된 경우 웹사이트에 요청 보내기
            if classNames[cls] == "cats":
                data = {
                    "class": "cats",
                    "confidence": confidence,
                    "box": [x1, y1, x2, y2]
                }
                # POST 요청 보내기
                check = input("Request? [Y/N] : ")

                if check == "Y":
                    response = requests.put(f"{target_url}/37.5881014/126.7126572")

                    print(f"Request sent to {target_url}: {response.status_code}")
                else:
                    print("Sleep 5 Second")
                    time.sleep(5)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()