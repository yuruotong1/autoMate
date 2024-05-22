from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import torch
from utils.qt_util import QtUtil


def gemma():
    print(torch.version)
   # 项目根目录
    model_path = os.path.join(QtUtil.get_root_path(), "agent", "model")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
    while True:
        input_text = input("请输入问题？")
        input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
        outputs = model.generate(**input_ids, max_length=512)
        print(tokenizer.decode(outputs[0])) 

if __name__ == "__main__":
    gemma()

