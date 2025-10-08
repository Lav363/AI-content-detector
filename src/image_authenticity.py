from transformers import pipeline
import os
from PIL import Image

# Initialize the image classification pipeline with a specialized model
# The first time this runs, it will download the model (a few hundred MB)
try:
    image_detector = pipeline("image-classification", model="umm-maybe/AI-image-detector")
except Exception as e:
    print(f"Could not load model. Make sure you have an internet connection. Error: {e}")
    image_detector = None

def check_image_authenticity(image_path):
    """
    Checks if an image is likely human-created or AI-generated.

    Args:
        image_path (str): The path to the image file.

    Returns:
        tuple: A tuple containing the label ('Human-created' or 'AI-generated image')
               and the confidence score.
    """
    if not image_detector:
        return "Error: Model not loaded", 0.0
    if not os.path.exists(image_path):
        return "Error: File not found", 0.0

    try:
        # Open the image to ensure it's a valid image file
        image = Image.open(image_path)
        
        # The pipeline returns a list of predictions
        predictions = image_detector(image)
        
        # The top prediction is the first element
        top_prediction = predictions[0]
        
        # Standardize the labels to match our project's requirements
        label = "AI-generated image" if top_prediction['label'] == 'artificial' else "Human-created"
        score = top_prediction['score']
        
        return label, score

    except Exception as e:
        return f"Error processing image: {e}", 0.0

# --- Example Usage for testing this module directly ---
if __name__ == "__main__":
    # IMPORTANT: Update these paths with your test images
    
    # Use a real figure you extracted in a previous step
    sample_real_image_path = "figures_output/figure_8_p12.png"
    
    # Find or create an AI-generated image for this test
    sample_ai_image_path = "download.png"

    print("--- AI Image Authenticity Check ---")

    if image_detector:
        # Test the real image
        if os.path.exists(sample_real_image_path):
            real_label, real_score = check_image_authenticity(sample_real_image_path)
            print(f"Analysis of '{sample_real_image_path}' (real):")
            print(f"-> Predicted Class: '{real_label}' (Confidence: {real_score:.2f})")
        else:
            print(f"Warning: Real test image not found at '{sample_real_image_path}'")

        print("-" * 20)

        # Test the AI-generated image
        if os.path.exists(sample_ai_image_path):
            ai_label, ai_score = check_image_authenticity(sample_ai_image_path)
            print(f"Analysis of '{sample_ai_image_path}' (AI):")
            print(f"-> Predicted Class: '{ai_label}' (Confidence: {ai_score:.2f})")
        else:
            print(f"Warning: AI test image not found at '{sample_ai_image_path}'")
            print("Please find an AI-generated image and update the path to test this feature.")