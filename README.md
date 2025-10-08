AI Content Detection & Visuals Unlocker for Scholarly Articles

<<<<<<< HEAD
     This project is an integrated tool designed to analyze scholarly articles in PDF format for authenticity and to extract and analyze visual content. It provides a comprehensive report on AI-generated text and images, and creates structured metadata for all figures found within the document.

📜 Project Overview

      The rise of sophisticated generative AI allows for the instant creation of human-like text and realistic scientific images. Academic editors and peer reviewers currently lack an integrated tool to effectively vet scholarly articles for AI-generated content. This project provides a unified, scholarly-focused platform that can holistically assess a manuscript in a single, streamlined process, addressing the fragmentation of existing solutions.
=======
This project is an integrated tool designed to analyze scholarly articles in PDF format for authenticity and to extract and analyze visual content. It provides a comprehensive report on AI-generated text and images, and creates structured metadata for all figures found within the document.

📜 Project Overview

The rise of sophisticated generative AI allows for the instant creation of human-like text and realistic scientific images. Academic editors and peer reviewers currently lack an integrated tool to effectively vet scholarly articles for AI-generated content. This project provides a unified, scholarly-focused platform that can holistically assess a manuscript in a single, streamlined process, addressing the fragmentation of existing solutions.
>>>>>>> 9e65bb3add8db754f0750112128b3ba1d962fae1

✨ Features

    This tool is a web application built with Streamlit that provides the following analysis features:

Text Analysis (Original Project)

1. Statistical Analysis: Calculates perplexity and burstiness to identify statistical patterns common in AI-generated text.

2. AI-Generated Text Detection: Uses a fine-tuned RoBERTa model to classify the main body of text as human-written or AI-generated.

3. Fact-Checking Prototype: Extracts claims from the text and verifies them against an external knowledge base.

Visual Analysis (Integrated Project)

1. Figure & Caption Extraction: Automatically detects and extracts all figures and their corresponding captions from the PDF.


2. Table Detection & Parsing: Identifies figures that are tables and parses their content into a downloadable CSV format.


3. OCR for Embedded Text: Reads and extracts text that is embedded within the figures themselves (e.g., axis labels, annotations).

4. Metadata Enrichment: Generates rich metadata for each figure, including:

A predicted Category (e.g., 'chart', 'table', 'diagram').

A list of extracted Keywords from the caption.


Figure Complexity Scoring: Assigns a numerical Complexity Score to each figure based on its textual and visual features.


AI-Generated Image Detection: Runs an AI detection model on each figure to verify if it is likely Human-created or AI-generated.

Summary Visualization: Presents a high-level summary pie chart showing the ratio of human vs. AI-generated figures found in the document.

🛠️ Tech Stack

Language: Python

Web Framework: Streamlit

Core Libraries: PyTorch, Hugging Face Transformers, OpenCV, spaCy, PyMuPDF, Pandas, scikit-learn

System Dependencies: Tesseract OCR

⚙️ Setup and Installation
Follow these steps to set up and run the project locally.

1. Clone the repository:

git clone <your-repository-url>
cd ai-content-detector

3. Create and activate a virtual environment:
   
# Create the environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

3. Install Tesseract OCR Engine:

This step is critical. The Python library for OCR (pytesseract) requires the Tesseract engine to be installed on your system.

Download and run the installer from the official Tesseract repository.

During installation, make sure to check the box to "Add Tesseract to system PATH."

4. Install Python dependencies:
   
pip install -r requirements.txt

🚀 How to Run

Make sure your virtual environment is active.

Run the following command in your terminal:
streamlit run app.py

3.Your web browser will automatically open with the application running.

📁 Project Structure
<<<<<<< HEAD
        ai-content-detector/
        ├── .gitignore
        ├── app.py             # The Streamlit UI application
        ├── main.py            # Original entry point (for text analysis)
        ├── README.md          # This file
        ├── requirements.txt
        ├── src/
        │   ├── __init__.py
        │   ├── figure_extractor.py
        │   ├── image_authenticity.py
        │   ├── process_pdf.py
        │   ├── text_analyzer.py
        │   ├── model_detector.py
        │   ├── fact_checker.py
        │   └── visual_analyzer.py
        └── venv/
=======

                    ai-content-detector/
                    ├── .gitignore
                    ├── app.py             # The Streamlit UI application
                    ├── main.py            # Original entry point (for text analysis)
                    ├── README.md          # This file
                    ├── requirements.txt
                    ├── src/
                    │   ├── __init__.py
                    │   ├── figure_extractor.py
                    │   ├── image_authenticity.py
                    │   ├── process_pdf.py
                    │   ├── text_analyzer.py
                    │   ├── model_detector.py
                    │   ├── fact_checker.py
                    │   └── visual_analyzer.py
                    └── venv/
>>>>>>> 9e65bb3add8db754f0750112128b3ba1d962fae1

👥 Team

Team Name: Cosmic crew 


Lead: Meharaj Banu 


Members: Meharaj Banu R, Lavanya K, Mahabath Nisha M, Aarthi S 


Mentor: Aishwarya 
