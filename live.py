from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO("./models/cat-v3-430-imgs.pt")

<<<<<<< HEAD
# Open the video stream
stream_url = 'tcp://192.168.123.101:8888'
cap = cv2.VideoCapture(stream_url)

=======
# Define the RTSP stream URL
rtsp_url = 'rtsp://192.168.123.101:8080//'  # Your RTSP stream URL

# Open the video stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the video stream was successfully opened
>>>>>>> e07fc6e0bac9924c58566014af72d37b2ad241dc
if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit()

<<<<<<< HEAD
=======
# Continuously capture frames from the video stream
>>>>>>> e07fc6e0bac9924c58566014af72d37b2ad241dc
while True:
    # Read a frame from the stream
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame.")
        break

    # Perform object detection
    results = model(frame)

    # Process detection results
    for result in results:
        # Loop through each detected object
        for box in result.boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # Draw the bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Optional: Draw a label with the class name and probability
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            prob = box.conf[0]
            label = f"{class_name} {prob:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

<<<<<<< HEAD
    # Display the frame
=======
    # Display the frame with bounding boxes and labels
>>>>>>> e07fc6e0bac9924c58566014af72d37b2ad241dc
    cv2.imshow("Preview", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

<<<<<<< HEAD
# Release resources
=======
# Release the video capture and destroy all OpenCV windows
>>>>>>> e07fc6e0bac9924c58566014af72d37b2ad241dc
cap.release()
cv2.destroyAllWindows()
