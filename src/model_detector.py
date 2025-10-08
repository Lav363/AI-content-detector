from transformers import pipeline

# Load a pre-trained model from Hugging Face Hub
# This model is specifically trained to detect text from OpenAI's GPT models
# Note: The first time you run this, it will download the model (a few hundred MB)
detector = pipeline("text-classification", model="roberta-base-openai-detector")

def predict_text_class(text):
    """
    Uses a pre-trained RoBERTa model to classify text as Human or AI-generated.
    Returns the prediction label and score.
    """
    if not text.strip():
        return "Unknown", 0.0
        
    results = detector(text)
    # The model outputs 'Real' for human and 'Fake' for AI. Let's standardize this.
    prediction = results[0]
    label = "Human" if prediction['label'] == 'Real' else "AI-Generated"
    score = prediction['score']
    
    return label, score

# --- Example Usage ---
if __name__ == "__main__":
    ai_text = "The study of artificial intelligence is a cornerstone of modern computer science. The implications of this research are far-reaching and have the potential to revolutionize many industries. The development of advanced algorithms is crucial for progress in this field."
    human_text = "So, AI... it's everywhere now, right? It's weird. One minute you're just using it to find cat pictures, the next it's driving cars and writing articles. I wonder what's next. Honestly, it's a bit scary but also pretty cool."

    print("--- Pre-trained Model Detection ---")
    
    ai_label, ai_score = predict_text_class(ai_text)
    print(f"Analysis of AI Text: Predicted class is '{ai_label}' with a confidence of {ai_score:.2f}")

    human_label, human_score = predict_text_class(human_text)
    print(f"Analysis of Human Text: Predicted class is '{human_label}' with a confidence of {human_score:.2f}")