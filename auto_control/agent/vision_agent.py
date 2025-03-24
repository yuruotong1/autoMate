from typing import List
import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
from pydantic import BaseModel

class UIElement(BaseModel):
    element_id: int
    coordinates: list[float]

class VisionAgent:
    def __init__(self, yolo_model_path: str):
        """
        Initialize the vision agent
        
        Parameters:
            yolo_model_path: Path to YOLO model
        """
        # determine the available device and the best dtype
        # load the YOLO model
        self.yolo_model = YOLO(yolo_model_path)

        self.elements: List[UIElement] = []

    def __call__(self, image_path: str) -> List[UIElement]:
        """Process an image from file path."""
        # image = self.load_image(image_source)
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Vision agent: Failed to read image")
        return self.analyze_image(image)
    
    def _reset_state(self):
        """Clear previous analysis results"""
        self.elements = []

    def analyze_image(self, image: np.ndarray) -> List[UIElement]:
        """
        Process an image through all computer vision pipelines.
        
        Args:
            image: Input image in BGR format (OpenCV default)
            
        Returns:
            List of detected UI elements with annotations
        """
        self._reset_state()

        boxes = self._detect_objects(image)
        
        for idx in range(len(boxes)):
            new_element = UIElement(element_id=idx, 
                                    coordinates=boxes[idx])
            self.elements.append(new_element)

        return self.elements

    def _detect_objects(self, image: np.ndarray) -> tuple[list[np.ndarray], list]:
        """Run object detection pipeline"""
        results = self.yolo_model(image)[0]
        detections = sv.Detections.from_ultralytics(results)
        boxes = detections.xyxy

        if len(boxes) == 0:
            return []

        # Filter out boxes contained by others
        areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
        sorted_indices = np.argsort(-areas)  # Sort descending by area
        sorted_boxes = boxes[sorted_indices]

        keep_sorted = []
        for i in range(len(sorted_boxes)):
            contained = False
            for j in keep_sorted:
                box_b = sorted_boxes[j]
                box_a = sorted_boxes[i]
                if (box_b[0] <= box_a[0] and box_b[1] <= box_a[1] and
                    box_b[2] >= box_a[2] and box_b[3] >= box_a[3]):
                    contained = True
                    break
            if not contained:
                keep_sorted.append(i)

        # Map back to original indices
        keep_indices = sorted_indices[keep_sorted]
        filtered_boxes = boxes[keep_indices]
        return filtered_boxes
    

    