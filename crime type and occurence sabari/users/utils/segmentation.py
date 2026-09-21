"""
YOLOv8 Segmentation Module
Detects blood stains and broken glass using segmentation
"""

import cv2
import numpy as np
from ultralytics import YOLO

class CrimeSegmentation:
    def __init__(self):
        # Load YOLOv8 segmentation model
        self.model = YOLO('yolov8n-seg.pt')  # Segmentation model

        # Option to include broken glass in segmentation results
        self.include_broken_glass = False

    def segment_blood(self, image_path):
        """
        Detect blood-like regions using color segmentation
        Red color detection as proxy for blood
        """
        img = cv2.imread(image_path)
        if img is None:
            return None, {"error": "Could not read image"}

        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Red color range for blood detection
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])

        # Create masks
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        blood_mask = mask1 + mask2

        # Find contours
        contours, _ = cv2.findContours(blood_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        blood_regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Filter small noise
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(img, "Blood Stain", (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                blood_regions.append({
                    'type': 'blood',
                    'area': area,
                    'bbox': [x, y, w, h]
                })

        return img, {
            'blood_detected': len(blood_regions) > 0,
            'blood_regions': blood_regions,
            'count': len(blood_regions)
        }

    def segment_glass(self, image_path):
        """
        Detect broken glass using edge detection and texture analysis
        """
        img = cv2.imread(image_path)
        if img is None:
            return None, {"error": "Could not read image"}

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Edge detection for glass shards
        edges = cv2.Canny(gray, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        glass_regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 200:  # Filter small edges
                # Check if shape is irregular (broken glass characteristic)
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity < 0.5:  # Irregular shape
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)
                        cv2.putText(img, "Broken Glass", (x, y-10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                        glass_regions.append({
                            'type': 'glass',
                            'area': area,
                            'bbox': [x, y, w, h]
                        })

        return img, {
            'glass_detected': len(glass_regions) > 0,
            'glass_regions': glass_regions,
            'count': len(glass_regions)
        }

    def segment_all(self, image_path):
        """
        Run both blood and glass segmentation
        """
        # Blood detection
        img_blood, blood_results = self.segment_blood(image_path)

        # Glass detection on original image (disabled by default)
        if self.include_broken_glass:
            img_glass, glass_results = self.segment_glass(image_path)
        else:
            img_glass = None
            glass_results = {
                'glass_detected': False,
                'glass_regions': [],
                'count': 0
            }

        # Combine results
        img = cv2.imread(image_path)

        # Run YOLO segmentation for additional objects
        results = self.model(img)

        segmentation_data = []
        for result in results:
            if result.masks is not None:
                masks = result.masks.data.cpu().numpy()
                boxes = result.boxes

                for i, (mask, box) in enumerate(zip(masks, boxes)):
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0])

                    # Resize mask to image size
                    mask_resized = cv2.resize(mask, (img.shape[1], img.shape[0]))

                    # Create colored mask overlay
                    color_mask = np.zeros_like(img)
                    color_mask[mask_resized > 0.5] = [0, 255, 0]  # Green overlay

                    # Blend with original image
                    img = cv2.addWeighted(img, 1, color_mask, 0.3, 0)

                    segmentation_data.append({
                        'class': class_name,
                        'confidence': confidence,
                        'mask_area': np.sum(mask_resized > 0.5)
                    })

        # Combine all results
        combined_results = {
            'blood': blood_results,
            'glass': glass_results,
            'yolo_segments': segmentation_data,
            'total_segments': len(segmentation_data) + blood_results['count'] + glass_results['count']
        }

        return img, combined_results
