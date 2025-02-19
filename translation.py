# translation.py
from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, model_name="Helsinki-NLP/opus-mt-en-es"):
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        # Encode the input text
        inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate translation
        translated = model.generate(**inputs)
        
        # Decode the output
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        print(f"Error during translation: {e}")
        return None