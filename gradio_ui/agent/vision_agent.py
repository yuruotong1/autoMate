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
        初始化视觉代理
        
        参数:
            yolo_model_path: YOLO模型路径
            caption_model_path: 图像描述模型路径，默认为Florence-2
        """
        # 确定可用的设备和最佳数据类型
        self.device, self.dtype = self._get_optimal_device_and_dtype()
        print(f"使用设备: {self.device}, 数据类型: {self.dtype}")
        
        # 加载YOLO模型
        self.yolo_model = YOLO(yolo_model_path)
        
        # 加载图像描述模型和处理器
        self.caption_processor = AutoProcessor.from_pretrained(
            "microsoft/Florence-2-base", 
            trust_remote_code=True
        )
        
        # 根据设备类型加载模型
        try:
            print(f"正在加载图像描述模型: {caption_model_path}")
            if self.device.type == 'cuda':
                # CUDA设备使用float16
                self.caption_model = AutoModelForCausalLM.from_pretrained(
                    caption_model_path, 
                    torch_dtype=torch.float16,
                    trust_remote_code=True
                ).to(self.device)
            elif self.device.type == 'mps':
                # MPS设备使用float32（MPS对float16支持有限）
                self.caption_model = AutoModelForCausalLM.from_pretrained(
                    caption_model_path, 
                    torch_dtype=torch.float32,
                    trust_remote_code=True
                ).to(self.device)
            else:
                # CPU使用float32
                self.caption_model = AutoModelForCausalLM.from_pretrained(
                    caption_model_path, 
                    torch_dtype=torch.float32,
                    trust_remote_code=True
                ).to(self.device)
            
            print("图像描述模型加载成功")
        except Exception as e:
            print(f"加载图像描述模型失败: {e}")
        
        # 设置提示词
        self.prompt = "<CAPTION>"
        
        # 设置批处理大小
        if self.device.type == 'cuda':
            self.batch_size = 128  # CUDA设备使用较大批处理大小
        elif self.device.type == 'mps':
            self.batch_size = 32   # MPS设备使用中等批处理大小
        else:
            self.batch_size = 16   # CPU使用较小批处理大小

        self.elements: List[UIElement] = []
        self.ocr_reader = easyocr.Reader(['en', 'ch_sim'])

    def __call__(self, image_path: str) -> List[UIElement]:
        """Process an image from file path."""
        # image = self.load_image(image_source)
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Vision agent: 图片读取失败")
        return self.analyze_image(image)
    
    def _get_optimal_device_and_dtype(self):
        """确定最佳设备和数据类型"""
        if torch.cuda.is_available():
            device = torch.device("cuda")
            # 检查GPU是否适合使用float16
            capability = torch.cuda.get_device_capability()
            gpu_name = torch.cuda.get_device_name()
            print(f"检测到CUDA设备: {gpu_name}, 计算能力: {capability}")
            
            # 只在较新的GPU上使用float16
            if capability[0] >= 7:  # Volta及以上架构
                dtype = torch.float16
                print("使用float16精度")
            else:
                dtype = torch.float32
                print("GPU计算能力较低，使用float32精度")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = torch.device("mps")
            dtype = torch.float32  # MPS上使用float32更安全
            print("检测到MPS设备(Apple Silicon)，使用float32精度")
        else:
            device = torch.device("cpu")
            dtype = torch.float32
            print("未检测到GPU，使用CPU和float32精度")
        
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
        """获取图像元素的描述"""
        if not element_crops:
            return []
        
        # 如果未指定批处理大小，使用实例的默认值
        if batch_size is None:
            batch_size = self.batch_size
        
        # 调整图像尺寸为64x64
        resized_crops = []
        for img in element_crops:
            # 转换为numpy数组，调整大小，再转回PIL
            img_np = np.array(img)
            resized_np = cv2.resize(img_np, (64, 64))
            resized_crops.append(Image.fromarray(resized_np))
        
        generated_texts = []
        device = self.device
        
        # 分批处理
        for i in range(0, len(resized_crops), batch_size):
            batch = resized_crops[i:i+batch_size]
            try:
                # 根据设备类型选择数据类型
                if device.type == 'cuda':
                    inputs = self.caption_processor(
                        images=batch, 
                        text=[self.prompt] * len(batch), 
                        return_tensors="pt",
                        do_resize=False  # 避免处理器改变图像尺寸
                    ).to(device=device, dtype=torch.float16)
                else:
                    # MPS和CPU使用float32
                    inputs = self.caption_processor(
                        images=batch, 
                        text=[self.prompt] * len(batch), 
                        return_tensors="pt"
                    ).to(device=device)
                
                # 针对Florence-2的特殊处理
                with torch.no_grad():
                    if 'florence' in self.caption_model.config.model_type:
                        generated_ids = self.caption_model.generate(
                            input_ids=inputs["input_ids"],
                            pixel_values=inputs["pixel_values"],
                            max_new_tokens=20,
                            num_beams=1, 
                            do_sample=False
                        )
                    else:
                        generated_ids = self.caption_model.generate(
                            **inputs, 
                            max_length=50,
                            num_beams=3,
                            early_stopping=True
                        )
                
                # 解码生成的ID
                texts = self.caption_processor.batch_decode(
                    generated_ids, 
                    skip_special_tokens=True
                )
                texts = [text.strip() for text in texts]
                generated_texts.extend(texts)
                
                # 清理缓存
                if device.type == 'cuda' and torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    
            except RuntimeError as e:
                print(f"批次处理失败: {e}")    
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
            # 处理可能存在的Data URL前缀（如 "data:image/png;base64,"）
            if ',' in image_source:
                _, payload = image_source.split(',', 1)
            else:
                payload = image_source

            # Base64解码 -> bytes -> numpy数组
            image_bytes = base64.b64decode(payload)
            np_array = np.frombuffer(image_bytes, dtype=np.uint8)
            
            # OpenCV解码图像
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("解码图片失败：无效的图片数据")
            
            return self.analyze_image(image)

        except (base64.binascii.Error, ValueError) as e:
            # 生成更清晰的错误信息
            error_msg = f"输入既不是有效的文件路径，也不是有效的Base64图片数据"
            raise ValueError(error_msg) from e


    

    