from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def rewrite_text(original_text, tone):
    prompt = (f"Rewrite the following sentence to have a {tone} tone. "
              f"Make sure the style and wording reflect the tone clearly.\n"
              f"Sentence: \"{original_text}\"")
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=True,
        top_p=0.9,
        top_k=50,
        temperature=0.8,
        num_return_sequences=1
    )
    rewritten = tokenizer.decode(output[0], skip_special_tokens=True)
    return rewritten