# translation.py
from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, model_name="Helsinki-NLP/opus-mt-en-es"):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    translated = model.generate(**tokenizer.prepare_seq2seq_batch([text], return_tensors="pt"))
    return [tokenizer.decode(t, skip_special_tokens=True) for t in translated][0]