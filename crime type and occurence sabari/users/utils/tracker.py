"""
DeepSORT Tracker Module
Tracks persons and assigns unique IDs
"""

import cv2
import numpy as np
from collections import defaultdict

class SimpleTracker:
    """
    Simple object tracker using centroid tracking
    (DeepSORT requires additional dependencies, this is a lightweight alternative)
    """
    def __init__(self, max_disappeared=50):
        self.next_object_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared

    def register(self, centroid):
        """Register new object with unique ID"""
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        """Remove object from tracking"""
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, detections):
        """
        Update tracker with new detections
        detections: list of bounding boxes [x1, y1, x2, y2]
        """
        # If no detections, mark all as disappeared
        if len(detections) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        # Calculate centroids from bounding boxes
        input_centroids = np.zeros((len(detections), 2), dtype="int")
        for i, (x1, y1, x2, y2) in enumerate(detections):
            cx = int((x1 + x2) / 2.0)
            cy = int((y1 + y2) / 2.0)
            input_centroids[i] = (cx, cy)

        # If no objects being tracked, register all
        if len(self.objects) == 0:
            for centroid in input_centroids:
                self.register(centroid)
        else:
            # Match existing objects to new detections
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            # Calculate distance between existing and new centroids
            distances = np.zeros((len(object_centroids), len(input_centroids)))
            for i, obj_centroid in enumerate(object_centroids):
                for j, input_centroid in enumerate(input_centroids):
                    distances[i, j] = np.linalg.norm(obj_centroid - input_centroid)

            # Find minimum distance matches
            rows = distances.min(axis=1).argsort()
            cols = distances.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue

                # If distance is reasonable, update object
                if distances[row, col] < 50:  # Threshold
                    object_id = object_ids[row]
                    self.objects[object_id] = input_centroids[col]
                    self.disappeared[object_id] = 0

                    used_rows.add(row)
                    used_cols.add(col)

            # Handle disappeared objects
            unused_rows = set(range(distances.shape[0])) - used_rows
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)

            # Register new objects
            unused_cols = set(range(distances.shape[1])) - used_cols
            for col in unused_cols:
                self.register(input_centroids[col])

        return self.objects


class PersonTracker:
    """
    Track persons in video and assign unique IDs
    """
    def __init__(self):
        self.tracker = SimpleTracker(max_disappeared=30)
        self.person_history = defaultdict(list)

    def track_persons(self, detections):
        """
        Track persons from YOLO detections
        detections: list of dicts with 'class' and 'bbox'
        """
        # Filter only person detections
        person_boxes = []
        for det in detections:
            if det['class'] == 'person':
                person_boxes.append(det['bbox'])

        # Update tracker
        tracked_objects = self.tracker.update(person_boxes)

        # Prepare tracking results
        tracking_results = []
        for object_id, centroid in tracked_objects.items():
            tracking_results.append({
                'id': object_id,
                'centroid': centroid.tolist(),
                'label': f"Person #{object_id}"
            })

            # Store history
            self.person_history[object_id].append(centroid)

        return tracking_results

    def draw_tracks(self, frame, tracked_objects, person_boxes):
        """
        Draw tracking information on frame
        """
        for i, (object_id, centroid) in enumerate(tracked_objects.items()):
            # Draw centroid
            cv2.circle(frame, tuple(centroid), 4, (0, 255, 0), -1)

            # Draw ID
            text = f"ID: {object_id}"
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Draw bounding box if available
            if i < len(person_boxes):
                x1, y1, x2, y2 = person_boxes[i]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw trajectory
            if object_id in self.person_history and len(self.person_history[object_id]) > 1:
                points = self.person_history[object_id]
                for j in range(1, len(points)):
                    if points[j - 1] is None or points[j] is None:
                        continue
                    cv2.line(frame, tuple(points[j - 1]), tuple(points[j]), (0, 255, 255), 2)

        return frame

    def get_tracking_summary(self):
        """
        Get summary of tracked persons
        """
        return {
            'total_persons_tracked': len(self.person_history),
            'currently_tracked': len(self.tracker.objects),
            'person_ids': list(self.person_history.keys())
        }
