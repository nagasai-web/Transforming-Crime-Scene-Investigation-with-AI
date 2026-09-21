"""
Enhanced Crime Detection Module
Detects: Blood, Broken Glass, Bullet Shells, Guns, Knives, Axes, Violence/Fight scenes
Uses specialized weapon detection model + custom detection algorithms
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os

class EnhancedCrimeDetector:
    def __init__(self):
        # Load specialized weapon detection model
        weapon_model_path = 'cs2-yolo12m-weapon-detection/cs2-yolo12m-weapon-detection.pt'
        if os.path.exists(weapon_model_path):
            self.weapon_model = YOLO(weapon_model_path)
        else:
            print("Warning: Specialized weapon model not found, using default YOLOv8")
            self.weapon_model = YOLO('yolov8n.pt')

        # Load general object detection model
        self.general_model = YOLO('yolov8n.pt')

        # Crime object classes
        self.weapon_classes = [
            'AK47', 'M4A1-S', 'M4A1', 'GALIL', 'FAMAS', 'TEC-9',
            'FIVE-SEVEN', 'GLOCK-18', 'USP-S', 'EAGLE', 'BERETTAS',
            'P2000', 'MAC10', 'MP5', 'MP9', 'P90', 'P250', 'SSG08', 'AWP',
            'knife', 'gun', 'rifle', 'pistol', 'axe'
        ]

        # COCO classes for general detection
        self.coco_weapon_classes = {
            43: 'knife',
            0: 'person'
        }

        # Option to include broken glass in prediction results
        self.include_broken_glass = False

    def detect_blood(self, image):
        """
        Detect blood stains using color segmentation
        Returns: mask, contours, count
        """
        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define range for red color (blood)
        # Red has two ranges in HSV
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        # Create masks
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        blood_mask = cv2.bitwise_or(mask1, mask2)

        # Morphological operations to remove noise
        kernel = np.ones((5, 5), np.uint8)
        blood_mask = cv2.morphologyEx(blood_mask, cv2.MORPH_CLOSE, kernel)
        blood_mask = cv2.morphologyEx(blood_mask, cv2.MORPH_OPEN, kernel)

        # Find contours
        contours, _ = cv2.findContours(blood_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter small contours (noise)
        min_area = 100
        blood_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

        return blood_mask, blood_contours, len(blood_contours)

    def detect_broken_glass(self, image):
        """
        Detect broken glass using edge detection and texture analysis
        Returns: mask, contours, count
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Dilate edges to connect fragments
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours based on shape (glass fragments are irregular)
        glass_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 200:  # Minimum area threshold
                perimeter = cv2.arcLength(cnt, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    # Glass fragments are irregular (low circularity)
                    if circularity < 0.7:
                        glass_contours.append(cnt)

        return dilated, glass_contours, len(glass_contours)

    def detect_bullet_shells(self, image):
        """
        Detect bullet shells using shape and color detection
        Returns: detections list
        """
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Detect metallic/golden color (bullet shells)
        lower_gold = np.array([15, 100, 100])
        upper_gold = np.array([35, 255, 255])

        mask = cv2.inRange(hsv, lower_gold, upper_gold)

        # Morphological operations
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bullet_shells = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 50 < area < 5000:  # Size range for bullet shells
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = float(w) / h if h > 0 else 0
                # Bullet shells are roughly circular or cylindrical
                if 0.5 < aspect_ratio < 2.0:
                    bullet_shells.append({
                        'bbox': [x, y, x+w, y+h],
                        'confidence': 0.75,
                        'class': 'bullet_shell'
                    })

        return bullet_shells

    def detect_violence(self, image):
        """
        Detect violence/fight scenes using pose estimation and motion analysis
        Returns: violence_score, indicators
        """
        # Run pose detection
        results = self.general_model(image)

        violence_indicators = []
        person_count = 0
        close_proximity_count = 0

        person_boxes = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                if class_id == 0:  # Person class
                    person_count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    person_boxes.append([x1, y1, x2, y2])

        # Check for close proximity (potential fight)
        for i in range(len(person_boxes)):
            for j in range(i+1, len(person_boxes)):
                box1 = person_boxes[i]
                box2 = person_boxes[j]

                # Calculate distance between centers
                center1 = [(box1[0]+box1[2])/2, (box1[1]+box1[3])/2]
                center2 = [(box2[0]+box2[2])/2, (box2[1]+box2[3])/2]

                distance = np.sqrt((center1[0]-center2[0])**2 + (center1[1]-center2[1])**2)

                # If persons are very close
                if distance < 100:
                    close_proximity_count += 1
                    violence_indicators.append("Close proximity detected")

        # Violence score calculation
        violence_score = 0
        if person_count >= 2 and close_proximity_count > 0:
            violence_score = min(close_proximity_count * 30, 100)
            violence_indicators.append(f"{person_count} persons in close proximity")

        return violence_score, violence_indicators

    def detect_all(self, image_path):
        """
        Comprehensive detection: weapons, blood, glass, bullet shells, violence
        Returns: annotated image, complete detection results
        """
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return None, {"error": "Could not read image"}

        original_img = img.copy()

        # Initialize results
        all_detections = {
            'weapons': [],
            'blood': [],
            'broken_glass': [],
            'bullet_shells': [],
            'persons': [],
            'violence': {},
            'risk_level': 'NORMAL'
        }

        # 1. Detect weapons using specialized model
        weapon_results = self.weapon_model(img)
        weapon_count = 0

        for result in weapon_results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                try:
                    class_name = self.weapon_model.names[class_id]
                except:
                    class_name = f"weapon_{class_id}"

                weapon_count += 1

                # Draw red box for weapons
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                label = f"{class_name}: {confidence:.2f}"
                cv2.putText(img, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                all_detections['weapons'].append({
                    'class': class_name,
                    'confidence': confidence,
                    'bbox': [x1, y1, x2, y2]
                })

        # 2. Detect persons using general model
        general_results = self.general_model(img)
        person_count = 0

        for result in general_results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                if class_id == 0:  # Person
                    person_count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])

                    # Draw green box for persons
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"person: {confidence:.2f}"
                    cv2.putText(img, label, (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    all_detections['persons'].append({
                        'confidence': confidence,
                        'bbox': [x1, y1, x2, y2]
                    })

        # 3. Detect blood
        blood_mask, blood_contours, blood_count = self.detect_blood(original_img)
        if blood_count > 0:
            cv2.drawContours(img, blood_contours, -1, (255, 0, 255), 2)
            for i, cnt in enumerate(blood_contours):
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.putText(img, "BLOOD", (cx-20, cy),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

                    x, y, w, h = cv2.boundingRect(cnt)
                    all_detections['blood'].append({
                        'bbox': [x, y, x+w, y+h],
                        'area': cv2.contourArea(cnt)
                    })

        # 4. Detect broken glass (disabled by default)
        if self.include_broken_glass:
            glass_mask, glass_contours, glass_count = self.detect_broken_glass(original_img)
        else:
            glass_mask, glass_contours, glass_count = None, [], 0

        if self.include_broken_glass and glass_count > 0:
            cv2.drawContours(img, glass_contours, -1, (255, 255, 0), 2)
            for i, cnt in enumerate(glass_contours):
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.putText(img, "GLASS", (cx-20, cy),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

                    x, y, w, h = cv2.boundingRect(cnt)
                    all_detections['broken_glass'].append({
                        'bbox': [x, y, x+w, y+h],
                        'area': cv2.contourArea(cnt)
                    })

        # 5. Detect bullet shells
        bullet_shells = self.detect_bullet_shells(original_img)
        for shell in bullet_shells:
            x1, y1, x2, y2 = shell['bbox']
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 165, 255), 2)
            cv2.putText(img, "BULLET SHELL", (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
            all_detections['bullet_shells'].append(shell)

        # 6. Detect violence/fight scenes
        violence_score, violence_indicators = self.detect_violence(original_img)
        all_detections['violence'] = {
            'score': violence_score,
            'indicators': violence_indicators
        }

        # 7. Calculate overall risk level
        risk_level = self.calculate_comprehensive_risk(
            person_count, weapon_count, blood_count,
            glass_count, len(bullet_shells), violence_score
        )
        all_detections['risk_level'] = risk_level

        # Add risk level banner
        risk_color = (0, 0, 255) if risk_level == "CRITICAL" else \
                     (0, 100, 255) if risk_level == "HIGH RISK" else \
                     (0, 255, 255) if risk_level == "MEDIUM RISK" else (0, 255, 0)

        cv2.rectangle(img, (10, 10), (300, 60), risk_color, -1)
        cv2.putText(img, f"RISK: {risk_level}", (20, 45),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Add detection summary
        summary_y = 80
        cv2.putText(img, f"Weapons: {weapon_count}", (10, summary_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(img, f"Persons: {person_count}", (10, summary_y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(img, f"Blood: {blood_count}", (10, summary_y + 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(img, f"Glass: {glass_count}", (10, summary_y + 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(img, f"Shells: {len(bullet_shells)}", (10, summary_y + 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Add counts to results
        all_detections['counts'] = {
            'weapons': weapon_count,
            'persons': person_count,
            'blood': blood_count,
            'broken_glass': glass_count,
            'bullet_shells': len(bullet_shells),
            'violence_score': violence_score
        }

        return img, all_detections

    def calculate_comprehensive_risk(self, person_count, weapon_count,
                                     blood_count, glass_count, shell_count, violence_score):
        """
        Calculate comprehensive risk level based on all detections
        """
        # Critical conditions
        if blood_count > 0 and weapon_count > 0 and person_count > 0:
            return "CRITICAL"

        if violence_score > 60:
            return "CRITICAL"

        if weapon_count > 2 or (weapon_count > 0 and person_count > 2):
            return "CRITICAL"

        # High risk conditions
        if weapon_count > 0 and person_count > 0:
            return "HIGH RISK"

        if blood_count > 2 or shell_count > 3:
            return "HIGH RISK"

        if violence_score > 30:
            return "HIGH RISK"

        # Medium risk conditions
        if weapon_count > 0 or blood_count > 0 or shell_count > 0:
            return "MEDIUM RISK"

        if glass_count > 3 or violence_score > 0:
            return "MEDIUM RISK"

        if person_count > 5:
            return "MEDIUM RISK"

        return "NORMAL"

    def detect_video(self, video_path, output_path):
        """
        Process video with comprehensive detection
        """
        cap = cv2.VideoCapture(video_path)

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        total_detections = {
            'weapons': 0,
            'persons': 0,
            'blood': 0,
            'glass': 0,
            'shells': 0,
            'violence_frames': 0
        }

        # Process every 3rd frame for speed
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % 3 == 0:  # Process every 3rd frame
                # Save frame temporarily
                temp_path = 'temp_frame.jpg'
                cv2.imwrite(temp_path, frame)

                # Run detection
                annotated_frame, results = self.detect_all(temp_path)

                if annotated_frame is not None:
                    frame = annotated_frame

                    # Accumulate detections
                    total_detections['weapons'] += results['counts']['weapons']
                    total_detections['persons'] += results['counts']['persons']
                    total_detections['blood'] += results['counts']['blood']
                    total_detections['glass'] += results['counts']['broken_glass']
                    total_detections['shells'] += results['counts']['bullet_shells']
                    if results['counts']['violence_score'] > 0:
                        total_detections['violence_frames'] += 1

                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            # Add frame counter
            cv2.putText(frame, f"Frame: {frame_count}", (width - 200, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            out.write(frame)
            frame_count += 1

        cap.release()
        out.release()

        return {
            'frames_processed': frame_count,
            'detections': total_detections,
            'output_video': output_path
        }
