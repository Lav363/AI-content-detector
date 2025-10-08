import os
from src.process_pdf import process_scholarly_pdf
from src.text_analyzer import calculate_perplexity, calculate_burstiness
from src.model_detector import predict_text_class
from src.fact_checker import extract_claim, retrieve_evidence, verify_claim

def analyze_document(pdf_path):
    """
    Runs a full analysis on a given PDF document.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return

    print(f"--- Starting Full Analysis of: {os.path.basename(pdf_path)} ---")

    # Step 1: Process the PDF to get text
    # Note: For this, we'll read the text from the output file.
    output_folder = "processed_output"
    process_scholarly_pdf(pdf_path, output_folder)
    
    text_path = os.path.join(output_folder, "full_text.txt")
    with open(text_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Analyze only the first 500 words for efficiency
    text_to_analyze = " ".join(full_text.split()[:500])

    print("\n[1] Statistical Analysis:")
    perplexity = calculate_perplexity(text_to_analyze)
    burstiness = calculate_burstiness(text_to_analyze)
    print(f"-> Perplexity Score: {perplexity:.2f}")
    print(f"-> Burstiness Score: {burstiness:.2f}")
    
    print("\n[2] Pre-trained Model Detection:")
    label, score = predict_text_class(text_to_analyze)
    print(f"-> Predicted Class: '{label}' (Confidence: {score:.2f})")
    
    print("\n[3] Fact-Checking Prototype:")
    claim = extract_claim(text_to_analyze)
    if claim:
        print(f"-> Extracted Claim for Fact-Checking: '{claim}'")
        evidence, url = retrieve_evidence(claim)
        if evidence:
            most_similar, sim_score = verify_claim(claim, evidence)
            print(f"-> Similarity to Evidence: {sim_score:.2f}")
            print(f"-> Most Relevant Fact: '{most_similar.strip()}'")
            print(f"-> Source: {url}")
        else:
            print("-> Could not find evidence for the claim.")
    else:
        print("-> No claim extracted.")
    
    print("\n--- Analysis Complete ---")


if __name__ == "__main__":
    # Replace this with the path to a PDF you downloaded
    # Try one human-written paper and one paper where you replaced the abstract with AI text
    sample_pdf_path = "The Role of Artificial Intelligence in Everyday Life.pdf"
    analyze_document(sample_pdf_path)