# --- granite_nlp.py ---
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the IBM Granite model
model_id = "ibm/granite-13b-instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.float16, device_map="auto"
)

def granite_rewrite(prompt: str, instruction: str = "Rewrite this text in a friendly tone"):
    full_prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{prompt}\n\n### Response:\n"
    inputs = tokenizer(full_prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=256)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result.split("### Response:")[-1].strip()
