from typing import List, Optional
import cv2
import torch
from ultralytics import YOLO
from transformers import AutoModelForCausalLM, AutoProcessor
import easyocr
import supervision as sv
import numpy as np
import time
from pydantic import BaseModel

class UIElement(BaseModel):
    element_id: int
    coordinates: list[float]
    caption: Optional[str] = None
    text: Optional[str] = None

class VisionAgent:
    def __init__(self, yolo_model_path: str, caption_model_path: str = 'microsoft/Florence-2-base-ft'):
        """
        Computer vision agent for UI analysis.
        
        Args:
            yolo_model_path: Path to YOLO model weights
            caption_model_path: Name/path to captioning model (defaults to Florence-2)
        """
        self.device = self._get_available_device()
        self.dtype = self._get_dtype()
        self.elements: List[UIElement] = []
        
        self.yolo_model = YOLO(yolo_model_path)
        self.caption_model = AutoModelForCausalLM.from_pretrained(
            caption_model_path, trust_remote_code=True
        ).to(self.device)
        self.caption_processor = AutoProcessor.from_pretrained(
            "microsoft/Florence-2-base", trust_remote_code=True
        )
        self.ocr_reader = easyocr.Reader(['en', 'ch_sim'])
        
    def _get_available_device(self) -> str:
        if torch.cuda.is_available():
            return 'cuda'
        if torch.backends.mps.is_available():
            return 'mps'
        return 'cpu'
    
    def _get_dtype(self)-> torch.dtype:
        if torch.cuda.is_available():
            return torch.float16
        return torch.float32

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
        
        element_crops, boxes = self._detect_objects(image)
        start = time.time()
        element_texts = self._extract_text(element_crops)
        end = time.time()
        ocr_time = (end-start) * 10 ** 3
        print(f"Speed: {ocr_time:.2f} ms OCR of {len(element_texts)} icons.")
        start = time.time()
        element_captions = self._get_caption(element_crops)
        end = time.time()
        caption_time = (end-start) * 10 ** 3
        print(f"Speed: {caption_time:.2f} ms captioning of {len(element_captions)} icons.")
        for idx in range(len(element_crops)):
            print(idx, boxes[idx], element_texts[idx], element_captions[idx])
            new_element = UIElement(element_id=idx, 
                                    coordinates=boxes[idx], 
                                    text=element_texts[idx][0] if len(element_texts[idx]) > 0 else '', 
                                    caption=element_captions[idx]
                                    )
            self.elements.append(new_element)
        
        return self.elements
    
    def _extract_text(self, images: np.ndarray) -> list[str]:
        """
        Run OCR in sequential mode
        TODO: It is possible to run in batch mode for a speed up, but the result quality needs test.
        https://github.com/JaidedAI/EasyOCR/pull/458
        """
        texts = []
        for image in images:
            text = self.ocr_reader.readtext(image, detail=0, paragraph=True, text_threshold=0.85)
            texts.append(text)
        # print(texts)
        return texts
        

    def _get_caption(self, images: np.ndarray, batch_size: int = 1) -> list[str]:
        """Run captioning in batched mode to avoid memory overflow"""
        prompt = "<CAPTION>"
        generated_texts = []
        resized_images = []
        for image in images:
            resized_image = cv2.resize(image, (64, 64))
            resized_images.append(resized_image)

        for i in range(0, len(resized_images), batch_size):
            batch_images = resized_images[i:i+batch_size]
            inputs = self.caption_processor(
                images=batch_images,
                text=[prompt] * len(batch_images),
                return_tensors="pt",
                do_resize=True,
            ).to(device=self.device, dtype=self.dtype)
            
            generated_ids = self.caption_model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=10,
                num_beams=1,
                do_sample=False,
                early_stopping=False,
            )
            
            generated_text = self.caption_processor.batch_decode(
                generated_ids, skip_special_tokens=True
            )
            generated_texts.extend([gen.strip() for gen in generated_text])
        
        return generated_texts


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
        
        # Extract element crops
        element_crops = []
        for box in filtered_boxes:
            x1, y1, x2, y2 = map(int, map(round, box))
            element = image[y1:y2, x1:x2]
            element_crops.append(np.array(element))
        
        return element_crops, filtered_boxes


    def __call__(self, image_path: str) -> List[UIElement]:
        """Process an image from file path."""
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not load image from {image_path}")
            
        return self.analyze_image(image)
        
    


        
image_path = 'imgs/mac_apps.png'
vision_agent = VisionAgent(yolo_model_path='weights/icon_detect/model.pt', caption_model_path='weights/icon_caption')
res = vision_agent(image_path)
print(res)
