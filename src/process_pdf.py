import fitz  # PyMuPDF
import os
import io
from PIL import Image

def process_scholarly_pdf(pdf_path, output_folder="processed_output"):
    """
    Extracts text and images from a given scholarly PDF file.

    Args:
        pdf_path (str): The file path to the PDF.
        output_folder (str): The folder to save extracted content.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        os.makedirs(os.path.join(output_folder, "images"))

    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        print(f"Successfully opened '{pdf_path}'. It has {doc.page_count} pages.")

        # 1. Extract Full Text
        full_text = ""
        for page_num, page in enumerate(doc):
            full_text += page.get_text("text") + "\n" # Add a newline between pages

        text_output_path = os.path.join(output_folder, "full_text.txt")
        with open(text_output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Full text saved to '{text_output_path}'")

        # 2. Extract Images
        image_count = 0
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)

            if not image_list:
                continue

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Get the image extension
                image_ext = base_image["ext"]
                
                # Load it to PIL
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Save the image
                    image_filename = f"image_p{page_num+1}_{img_index+1}.{image_ext}"
                    image_path = os.path.join(output_folder, "images", image_filename)
                    image.save(open(image_path, "wb"))
                    image_count += 1
                except Exception as e:
                    print(f"Warning: Could not process an image on page {page_num+1}. Error: {e}")

        print(f"Extracted and saved {image_count} images.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'doc' in locals():
            doc.close()

# --- Example Usage ---
if __name__ == "__main__":
    # Create a dummy PDF path. Replace this with a real PDF you downloaded.
    # For example: sample_pdf = "./data/human_articles/some_arxiv_paper.pdf"
    sample_pdf = "2509.10564v1.pdf" 
    
    if os.path.exists(sample_pdf):
        process_scholarly_pdf(sample_pdf)
    else:
        print(f"Error: The file '{sample_pdf}' was not found.")
        print("Please download a scholarly article PDF and update the 'sample_pdf' variable in the script.")