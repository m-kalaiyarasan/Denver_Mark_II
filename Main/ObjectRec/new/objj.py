import cv2
import numpy as np

# Load YOLOv3 configuration and weights files
config_path = "yolov3.cfg"
weights_path = "yolov3.weights"
classes_file = "coco.names"

# Load the class labels
with open(classes_file, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Load YOLOv3 model
net = cv2.dnn.readNet(weights_path, config_path)

# Get the output layer names
layer_names = net.getLayerNames()
unconnected_out_layers = net.getUnconnectedOutLayers()

# Handle different formats of unconnected_out_layers
if isinstance(unconnected_out_layers, np.ndarray):
    unconnected_out_layers = unconnected_out_layers.flatten().tolist()
elif isinstance(unconnected_out_layers, list) and isinstance(unconnected_out_layers[0], np.ndarray):
    unconnected_out_layers = [item[0] for item in unconnected_out_layers]

output_layers = [layer_names[i - 1] for i in unconnected_out_layers]

# Set to store previously detected objects
previously_detected_classes = set()

# Function to perform object detection
def detect_objects(img):
    height, width, channels = img.shape

    # Prepare the image for YOLO
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    # Process each detected object
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:  # Confidence threshold
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-max suppression to remove overlapping boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw boxes and labels
    detected_classes = []
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            detected_classes.append(classes[class_ids[i]])

    return img, detected_classes

# Capture video from webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Detect objects in the frame
    detected_frame, detected_classes = detect_objects(frame)

    # Display the resulting frame
    cv2.imshow('Object Detection using YOLOv3', detected_frame)

    # Print detected object names if they are new
    new_detected_classes = set(detected_classes) - previously_detected_classes
    if new_detected_classes:
        print("Newly detected objects:", ", ".join(new_detected_classes))
        previously_detected_classes.update(new_detected_classes)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
