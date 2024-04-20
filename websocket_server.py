import cv2
import websockets
import asyncio
import base64
from ultralytics import YOLO

# 웹캠 시작
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# 모델
model = YOLO("models/cat-v3-430-imgs.pt")

# 객체 클래스
classNames = ["cats"]

# 웹소켓 서버
async def websocket_server(websocket, path):
    while True:
        # 웹캠에서 프레임 읽기
        success, img = cap.read()
        results = model(img, stream=True)

        # 이미지 처리
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # 좌표
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # 정수로 변환

                # 이미지에 사각형 그리기
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # 클래스 이름 추가
                cls = int(box.cls[0])
                cv2.putText(img, classNames[cls], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

        # 이미지를 JPEG 형식으로 인코딩
        _, jpeg = cv2.imencode('.jpg', img)
        jpeg_data = jpeg.tobytes()

        # 이미지를 base64로 인코딩
        jpeg_base64 = base64.b64encode(jpeg_data).decode('utf-8')

        # 클라이언트에게 전송
        await websocket.send(jpeg_base64)

        # 0.1초 대기
        await asyncio.sleep(0.1)

start_server = websockets.serve(websocket_server, "0.0.0.0", 8765)

# 서버 시작
asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket 서버가 시작되었습니다.")
asyncio.get_event_loop().run_forever()
