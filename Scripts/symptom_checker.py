import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Hugging Face model
MODEL_NAME = "your-huggingface-model-name"

def load_symptom_checker():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.to(device)
    model.eval()
    return model, tokenizer

symptom_model, symptom_tokenizer = load_symptom_checker()

def analyze_symptoms(symptom_text):
    """ Analyzes symptoms and provides possible conditions. """
    inputs = symptom_tokenizer(symptom_text, return_tensors="pt", padding=True, truncation=True)
    inputs = {key: val.to(device) for key, val in inputs.items()}

    with torch.no_grad():
        outputs = symptom_model(**inputs)
        predictions = torch.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(predictions).item()
        confidence = predictions[0, predicted_class].item()

    return f"Possible condition: {predicted_class} with confidence {confidence:.2%}"
