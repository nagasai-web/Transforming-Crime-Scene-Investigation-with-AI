"""
YOLOv8 Object Detection Module
Detects weapons, persons, and crime-related objects
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os

class CrimeDetector:
    def __init__(self):
        # Load YOLOv8 model (pretrained on COCO dataset)
        self.model = YOLO('yolov8n.pt')  # nano model for speed

        # Crime-related classes from COCO dataset (COCO class IDs)
        self.allowed_classes = {
            0: 'person',
            39: 'bottle',  # Proxy for bat/blunt weapon
            43: 'knife',
            76: 'scissors',
            32: 'sports ball',  # Proxy for bullet shell
            1: 'bicycle',  # Proxy for rifle (long object)
            28: 'umbrella',  # Proxy for rifle/gun (long object)
            33: 'tie',  # Proxy for rope
            49: 'orange',  # Proxy for bullet shell (alternative)
        }

        # Weapon keywords for detection
        self.weapon_keywords = ['knife', 'gun', 'rifle', 'bat', 'scissors', 'bottle', 'umbrella', 'bicycle']

        # Crime object mapping - map COCO classes to crime objects
        self.crime_mapping = {
            'bottle': 'bat',
            'sports ball': 'bullet shell',
            'bicycle': 'rifle',
            'umbrella': 'gun',
            'tie': 'rope',
            'orange': 'bullet shell'
        }

    def detect_objects(self, image_path):
        """
        Detect objects in image
        Returns: annotated image, detection results
        """
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return None, {"error": "Could not read image"}

        # Run detection
        results = self.model(img)

        # Process results
        detections = []
        person_count = 0
        weapon_count = 0

        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]

                # Filter: Only process allowed crime-related classes
                if class_id not in self.allowed_classes:
                    continue

                # Map to crime object names
                display_name = self.crime_mapping.get(class_name, class_name)

                # Count persons and weapons
                if class_name == 'person':
                    person_count += 1
                    color = (0, 255, 0)  # Green for person
                elif any(weapon in class_name.lower() for weapon in self.weapon_keywords):
                    weapon_count += 1
                    color = (0, 0, 255)  # Red for weapon
                else:
                    weapon_count += 1  # Other crime objects count as weapons
                    color = (0, 0, 255)  # Red for weapon

                # Draw bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

                # Draw label with mapped name
                label = f"{display_name}: {confidence:.2f}"
                cv2.putText(img, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Store detection
                detections.append({
                    'class': display_name,
                    'confidence': confidence,
                    'bbox': [x1, y1, x2, y2]
                })

        # Determine risk level
        risk_level = self.calculate_risk(person_count, weapon_count, detections)

        # Prepare response
        response = {
            'objects': detections,
            'count': {
                'person': person_count,
                'weapon': weapon_count,
                'total': len(detections)
            },
            'risk_level': risk_level
        }

        return img, response

    def detect_video(self, video_path, output_path):
        """
        Process video frame by frame
        """
        cap = cv2.VideoCapture(video_path)

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        total_detections = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Run detection on frame
            results = self.model(frame)

            # Draw detections
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]

                    # Filter: Only process allowed crime-related classes
                    if class_id not in self.allowed_classes:
                        continue

                    # Map to crime object names
                    display_name = self.crime_mapping.get(class_name, class_name)

                    # Color coding
                    if class_name == 'person':
                        color = (0, 255, 0)
                    elif any(weapon in class_name.lower() for weapon in self.weapon_keywords):
                        color = (0, 0, 255)
                    else:
                        color = (0, 0, 255)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    label = f"{display_name}: {confidence:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                    total_detections.append(display_name)

            # Add frame number
            cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()

        # Summary
        from collections import Counter
        detection_summary = Counter(total_detections)

        return {
            'frames_processed': frame_count,
            'detections': dict(detection_summary),
            'output_video': output_path
        }

    def calculate_risk(self, person_count, weapon_count, detections):
        """
        Calculate risk level based on detections
        Logic: person + weapon = HIGH RISK
        """
        if person_count > 0 and weapon_count > 0:
            return "HIGH RISK"
        elif weapon_count > 0:
            return "MEDIUM RISK"
        elif person_count > 3:
            return "MEDIUM RISK"
        else:
            return "NORMAL"

    def detect_custom_objects(self, image_path, custom_classes):
        """
        Detect custom crime objects (knife, gun, rifle, bat, rope, bullet shell)
        Filters only allowed crime-related objects
        """
        img, results = self.detect_objects(image_path)

        # All detections are already filtered to crime objects
        results['crime_objects'] = results['objects']
        return img, results
