from ultralytics import YOLO
import cv2
import math
import requests  # 추가된 라이브러리
import time

# 웹캠 시작
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 모델 로드
model = YOLO("models/cat-v3-430-imgs.pt")

# 객체 클래스
classNames = ["cats"]

# 감지된 "cats"를 보내고자 하는 웹사이트 URL
target_url = "http://localhost:8000/set"  # 여기에 요청을 보내고자 하는 URL을 입력하세요

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # 감지된 객체 처리
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # 바운딩 박스 좌표 추출
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # 정수 값으로 변환

            # 이미지에 바운딩 박스 표시
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # 신뢰도
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)

            # 클래스 이름
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # 객체 세부 정보
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
