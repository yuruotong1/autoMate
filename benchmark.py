from transformers import AutoProcessor, AutoModelForCausalLM 
import easyocr
from tqdm import tqdm
from PIL import Image
import torch

caption_model_path = 'weights/icon_caption'


if torch.cuda.is_available():
    device = 'cuda'
elif torch.backends.mps.is_available():
    device = 'mps'
else:
    device = 'cpu'
print(f"using device {device}")
model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-base-ft", trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-base-ft", trust_remote_code=True)
reader = easyocr.Reader(['en', 'ch_sim'])
image_path = 'imgs/mac_apps.png'
image = Image.open(image_path).convert("RGB")

for i in tqdm(range(1000)):
    result = reader.readtext(image_path, detail = 0, paragraph=True)
    print(result)


for i in tqdm(range(1000)):
    task_prompt = '<OCR>'
    inputs = processor(text=task_prompt, images=image, return_tensors="pt").to(device)
    generated_ids = model.generate(
        input_ids=inputs["input_ids"].to(device),
        pixel_values=inputs["pixel_values"].to(device),
        max_new_tokens=20,
        early_stopping=False,
        do_sample=False,
        num_beams=1,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(
        generated_text, 
        task=task_prompt, 
        image_size=(image.width, image.height)
    )

    print(parsed_answer)