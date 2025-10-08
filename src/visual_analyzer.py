import cv2
import numpy as np
import os
import pytesseract
import pandas as pd
import re
import spacy

# We need the OCR function from our other module for the test section
from .figure_extractor import ocr_text_from_image

# Load the spaCy model once when the script is loaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    nlp = None

def is_table(image_path, horiz_thresh=10, vert_thresh=15):
    """
    Detects if an image contains a table using stricter thresholds.
    """
    if not os.path.exists(image_path):
        return False
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    thresh = cv2.adaptiveThreshold(~image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    contours_h, _ = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detect_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    contours_v, _ = cv2.findContours(detect_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours_h) > horiz_thresh and len(contours_v) > vert_thresh:
        return True
    return False

def parse_table(image_path):
    """
    Parses a table from an image and returns its data as a list of lists.
    """
    # ... (code for this function is unchanged) ...
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh_value = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    dilated_image = cv2.dilate(thresh_value, None, iterations=2)
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    bounding_boxes.sort(key=lambda x: (x[1], x[0]))
    table_data = []
    current_row = []
    last_y = -1
    for (x, y, w, h) in bounding_boxes:
        if w < 20 or h < 20 or w > image.shape[1] * 0.8:
            continue
        cell_image = image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(cell_image, config='--psm 6').strip()
        if last_y != -1 and y > last_y + h * 0.5:
            table_data.append(current_row)
            current_row = []
        current_row.append(text)
        last_y = y
    if current_row:
        table_data.append(current_row)
    return table_data

def categorize_figure(image_path, ocr_text=""):
    """
    Categorizes a figure using the refined, smarter logic.
    """
    has_grid_structure = is_table(image_path)
    is_text_numeric = False
    if ocr_text:
        digits = sum(c.isdigit() for c in ocr_text)
        letters = sum(c.isalpha() for c in ocr_text)
        total_chars = digits + letters
        if total_chars > 10:
            digit_ratio = digits / total_chars
            if digit_ratio > 0.3:
                is_text_numeric = True
    if has_grid_structure and is_text_numeric:
        return "chart"
    elif has_grid_structure and not is_text_numeric:
        return "table"
    elif not has_grid_structure and is_text_numeric:
        return "chart"
    else:
        return "diagram / photo"

def extract_keywords(caption_text):
    """
    Extracts keywords using spaCy's noun_chunks for better results.
    """
    if not nlp:
        return []
    doc = nlp(caption_text)
    keywords = set()
    for chunk in doc.noun_chunks:
        keywords.add(chunk.text.lower())
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
            keywords.add(token.lemma_.lower())
    return sorted(list(keywords))

def estimate_complexity(image_path, ocr_text=""):
    """
    Estimates the complexity of a figure with tuned scaling factors.
    """
    # 1. Text Complexity (based on number of words)
    text_score = len(ocr_text.split()) / 15  # Tuned scaling factor
    
    # 2. Visual Complexity (based on number of contours/shapes)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    visual_score = len(contours) / 300 # Tuned scaling factor

    # Combine scores and cap at 10
    complexity_score = min(10.0, text_score + visual_score)
    return round(complexity_score, 2)

# --- Example Usage for testing this module directly ---
if __name__ == "__main__":
    sample_chart_image_path = "figures_output/figure_8_p12.png"
    sample_diagram_image_path = "figures_output/figure_7_p9.png"
    sample_caption = "Effect of temperature on protein folding"

    print("--- Figure Categorization Test ---")
    if os.path.exists(sample_chart_image_path):
        chart_ocr_text = ocr_text_from_image(sample_chart_image_path)
        category = categorize_figure(sample_chart_image_path, chart_ocr_text)
        print(f"Analysis of '{sample_chart_image_path}':")
        print(f"-> Detected Category: {category}")
    else:
        print(f"Warning: Test file not found at '{sample_chart_image_path}'")
    print("-" * 20)
    if os.path.exists(sample_diagram_image_path):
        diagram_ocr_text = ocr_text_from_image(sample_diagram_image_path)
        category = categorize_figure(sample_diagram_image_path, diagram_ocr_text)
        print(f"Analysis of '{sample_diagram_image_path}':")
        print(f"-> Detected Category: {category}")
    else:
        print(f"Warning: Test file not found at '{sample_diagram_image_path}'")
    
    print("\n--- Keyword Extraction Test ---")
    if nlp:
        keywords = extract_keywords(sample_caption)
        print(f"Caption: '{sample_caption}'")
        print(f"-> Extracted Keywords: {keywords}")

    print("\n--- Complexity Estimation Test ---")
    if os.path.exists(sample_chart_image_path) and os.path.exists(sample_diagram_image_path):
        chart_complexity = estimate_complexity(sample_chart_image_path, chart_ocr_text)
        diagram_complexity = estimate_complexity(sample_diagram_image_path, diagram_ocr_text)
        print(f"Complexity score for '{sample_chart_image_path}': {chart_complexity}")
        print(f"Complexity score for '{sample_diagram_image_path}': {diagram_complexity}")