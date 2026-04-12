import cv2
import numpy as np
import os
import urllib.request


class YOLODetector:
    """YOLOv3 detector for animal herd detection"""

    # Animal classes to detect
    ANIMAL_CLASSES = {
        'cow', 'sheep', 'horse', 'dog', 'cat', 'bird',
        'elephant', 'zebra', 'giraffe', 'bear'
    }

    def __init__(self, model_dir='yolo_models'):
        self.model_dir = model_dir
        self.weights_path = os.path.join(model_dir, 'yolov3.weights')
        self.cfg_path = os.path.join(model_dir, 'yolov3.cfg')
        self.names_path = os.path.join(model_dir, 'coco.names')

        # Ensure model directory exists
        os.makedirs(model_dir, exist_ok=True)

        # Download models if not present
        self._download_models()

        # Load YOLO
        self.net = cv2.dnn.readNet(self.weights_path, self.cfg_path)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        # Load class names
        with open(self.names_path, 'r') as f:
            self.class_names = [line.strip() for line in f.readlines()]

    def _download_models(self):
        """Download YOLOv3 models if not present"""
        files = {
            'yolov3.weights': [
                'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov3.weights',
                'https://pjreddie.com/media/files/yolov3.weights'
            ],
            'yolov3.cfg': [
                'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov3.cfg',
                'https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg'
            ],
            'coco.names': [
                'https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names',
                'https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names'
            ]
        }

        for filename, urls in files.items():
            filepath = os.path.join(self.model_dir, filename)
            if not os.path.exists(filepath):
                print(f"Downloading {filename}... (this may take a while on first run)")
                downloaded = False
                
                for url in urls:
                    try:
                        print(f"  Trying: {url.split('/')[-1]}...")
                        urllib.request.urlretrieve(url, filepath)
                        print(f"  ✓ Downloaded {filename}")
                        downloaded = True
                        break
                    except Exception as e:
                        print(f"  ✗ Failed: {str(e)[:50]}")
                        continue
                
                if not downloaded:
                    raise RuntimeError(f"Failed to download {filename} from all sources. Please check your internet connection.")

    def detect(self, image_path):
        """Detect animals in image and return annotated image with count"""
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")

        height, width, channels = image.shape

        # Prepare blob for YOLO
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        # Process detections
        class_ids = []
        confidences = []
        boxes = []
        animal_count = 0

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Filter by confidence threshold
                if confidence > 0.5:
                    class_name = self.class_names[class_id]

                    # Filter by animal classes only
                    if class_name.lower() in self.ANIMAL_CLASSES:
                        # Get box coordinates
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
                        animal_count += 1

        # Apply Non-Maximum Suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Draw bounding boxes and labels
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2

        filtered_animal_count = len(indices)

        for i in indices.flatten():
            x, y, w, h = boxes[i]
            class_id = class_ids[i]
            confidence = confidences[i]
            label = f"{self.class_names[class_id]}: {confidence:.2f}"

            # Draw bounding box (green for animals)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), thickness)

            # Draw label background
            (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
            cv2.rectangle(image, (x, y - text_height - baseline),
                         (x + text_width, y), (0, 255, 0), -1)

            # Put label text
            cv2.putText(image, label, (x, y - baseline), font, font_scale, (0, 0, 0), thickness)

        return image, filtered_animal_count

    def save_image(self, image, output_path):
        """Save annotated image"""
        cv2.imwrite(output_path, image)
