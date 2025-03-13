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
import base64
from PIL import Image

class UIElement(BaseModel):
    element_id: int
    coordinates: list[float]
    caption: Optional[str] = None
    text: Optional[str] = None

class VisionAgent:
    def __init__(self, yolo_model_path: str, caption_model_path: str = 'microsoft/Florence-2-base-ft'):
        """
        Initialize the vision agent
        
        Parameters:
            yolo_model_path: Path to YOLO model
            caption_model_path: Path to image caption model, default is Florence-2
        """
        # determine the available device and the best dtype
        self.device, self.dtype = self._get_optimal_device_and_dtype()        
        # load the YOLO model
        self.yolo_model = YOLO(yolo_model_path)
        
        # load the image caption model and processor
        self.caption_processor = AutoProcessor.from_pretrained(
            "microsoft/Florence-2-base", 
            trust_remote_code=True
        )
        
        # load the model according to the device type
        try:
            if self.device.type == 'cuda':
                # CUDA device uses float16
                self.caption_model = AutoModelForCausalLM.from_pretrained(
                    caption_model_path, 
                    torch_dtype=torch.float16,
                    trust_remote_code=True
                ).to(self.device)
            elif self.device.type == 'mps':
                # MPS device uses float32 (MPS has limited support for float16)
                self.caption_model = AutoModelForCausalLM.from_pretrained(
                    caption_model_path, 
                    torch_dtype=torch.float32,
                    trust_remote_code=True
                ).to(self.device)
            else:
                # CPU uses float32
                self.caption_model = AutoModelForCausalLM.from_pretrained(
                    caption_model_path, 
                    torch_dtype=torch.float32,
                    trust_remote_code=True
                ).to(self.device)
            
        except Exception as e:
            raise e
        self.prompt = "<CAPTION>"
        
        # set the batch size
        if self.device.type == 'cuda':
            self.batch_size = 128
        elif self.device.type == 'mps':
            self.batch_size = 32
        else:
            self.batch_size = 16

        self.elements: List[UIElement] = []
        self.ocr_reader = easyocr.Reader(['en', 'ch_sim'])

    def __call__(self, image_path: str) -> List[UIElement]:
        """Process an image from file path."""
        # image = self.load_image(image_source)
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Vision agent: Failed to read image")
        return self.analyze_image(image)
    
    def _get_optimal_device_and_dtype(self):
        """determine the optimal device and dtype"""
        if torch.cuda.is_available():
            device = torch.device("cuda")
            # check if the GPU is suitable for using float16
            capability = torch.cuda.get_device_capability()
            # only use float16 on newer GPUs
            if capability[0] >= 7: 
                dtype = torch.float16
            else:
                dtype = torch.float32
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = torch.device("mps")
            dtype = torch.float32 
        else:
            device = torch.device("cpu")
            dtype = torch.float32
        
        return device, dtype

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
        element_captions = self._get_caption(element_crops, 5)
        end = time.time()
        caption_time = (end-start) * 10 ** 3
        print(f"Speed: {caption_time:.2f} ms captioning of {len(element_captions)} icons.")
        for idx in range(len(element_crops)):
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

    def _get_caption(self, element_crops, batch_size=None):
        """get the caption of the element crops"""
        if not element_crops:
            return []
        
        # if batch_size is not specified, use the instance's default value
        if batch_size is None:
            batch_size = self.batch_size
        
        # resize the image to 64x64
        resized_crops = []
        for img in element_crops:
            # convert to numpy array, resize, then convert back to PIL
            img_np = np.array(img)
            resized_np = cv2.resize(img_np, (64, 64))
            resized_crops.append(Image.fromarray(resized_np))
        
        generated_texts = []
        device = self.device
        
        # process in batches
        for i in range(0, len(resized_crops), batch_size):
            batch = resized_crops[i:i+batch_size]
            try:
                # select the dtype according to the device type
                if device.type == 'cuda':
                    inputs = self.caption_processor(
                        images=batch, 
                        text=[self.prompt] * len(batch), 
                        return_tensors="pt",
                        do_resize=False
                    ).to(device=device, dtype=torch.float16)
                else:
                    # MPS and CPU use float32
                    inputs = self.caption_processor(
                        images=batch, 
                        text=[self.prompt] * len(batch), 
                        return_tensors="pt"
                    ).to(device=device)
                
                # special treatment for Florence-2
                with torch.no_grad():
                    if 'florence' in self.caption_model.config.model_type:
                        generated_ids = self.caption_model.generate(
                            input_ids=inputs["input_ids"],
                            pixel_values=inputs["pixel_values"],
                            max_new_tokens=20,
                            num_beams=5, 
                            do_sample=False
                        )
                    else:
                        generated_ids = self.caption_model.generate(
                            **inputs, 
                            max_length=50,
                            num_beams=3,
                            early_stopping=True
                        )
                
                # decode the generated IDs
                texts = self.caption_processor.batch_decode(
                    generated_ids, 
                    skip_special_tokens=True
                )
                texts = [text.strip() for text in texts]
                generated_texts.extend(texts)
                
                # clean the cache
                if device.type == 'cuda' and torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    
            except RuntimeError as e:
                raise e
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
    
    def load_image(self, image_source: str) -> np.ndarray:
        try:
            # Handle potential Data URL prefix (like "data:image/png;base64,")
            if ',' in image_source:
                _, payload = image_source.split(',', 1)
            else:
                payload = image_source

            # Base64 decode -> bytes -> numpy array
            image_bytes = base64.b64decode(payload)
            np_array = np.frombuffer(image_bytes, dtype=np.uint8)
            
            # OpenCV decode image
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Failed to decode image: Invalid image data")
            
            return self.analyze_image(image)

        except (base64.binascii.Error, ValueError) as e:
            # Generate clearer error message
            error_msg = f"Input is neither a valid file path nor valid Base64 image data"
            raise ValueError(error_msg) from e


    

    