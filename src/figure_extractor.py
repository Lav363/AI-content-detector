import fitz  # PyMuPDF
import os
import io
import pytesseract
import re
from PIL import Image

def ocr_text_from_image(image_path):
    """
    Performs OCR on a single image file to extract embedded text.
    """
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text.strip()
    except Exception as e:
        print(f"Error during OCR for {image_path}: {e}")
        return ""

def find_caption_for_image(page, img_bbox):
    """
    Finds the caption for a given image by searching for nearby text blocks.
    """
    # Search for text blocks that are below the image
    blocks = page.get_text("blocks")
    caption = ""
    min_dist = float('inf')

    for block in blocks:
        block_bbox = fitz.Rect(block[:4])
        block_text = block[4].strip()

        # Check if the block is below the image and not too far away
        if block_bbox.y0 > img_bbox.y1 and abs(block_bbox.x0 - img_bbox.x0) < 100:
            # Check if the text starts with a typical caption pattern (e.g., "Figure 1", "Fig. 1")
            if re.match(r'^(Figure|Fig\.?)\s*\d+', block_text, re.IGNORECASE):
                distance = block_bbox.y0 - img_bbox.y1
                if distance < min_dist:
                    min_dist = distance
                    caption = block_text
    
    return caption.replace("\n", " ")


def extract_figures(pdf_path, output_dir="figures_output"):
    """
    Extracts figures, their captions, and performs OCR on each figure.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = fitz.open(pdf_path)
    extracted_data = []
    figure_count = 0

    for page_num, page in enumerate(doc):
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            
            # Get the image's bounding box on the page
            img_bbox = page.get_image_bbox(img)

            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            try:
                image = Image.open(io.BytesIO(image_bytes))
                figure_count += 1
                figure_filename = f"figure_{figure_count}_p{page_num + 1}.png"
                save_path = os.path.join(output_dir, figure_filename)
                
                image.save(open(save_path, "wb"), "PNG")

                ocr_text = ocr_text_from_image(save_path)
                caption_text = find_caption_for_image(page, img_bbox)
                
                extracted_data.append({
                    "image_path": save_path,
                    "ocr_text": ocr_text,
                    "caption": caption_text
                })
            except Exception as e:
                print(f"Warning: Could not process image on page {page_num + 1}. Error: {e}")

    doc.close()
    print(f"Successfully extracted {len(extracted_data)} figures and their captions.")
    return extracted_data

# --- Example Usage for testing this module directly ---
if __name__ == "__main__":
    sample_pdf_path = "path_to_your_sample_paper.pdf"
    
    if os.path.exists(sample_pdf_path):
        print(f"Processing PDF: {sample_pdf_path}")
        figure_data = extract_figures(sample_pdf_path)
        
        for data in figure_data:
            print("\n--------------------")
            print(f"Figure Location: {data['image_path']}")
            print(f"Detected Caption: {data['caption']}")
            print(f"Text inside figure (OCR): {data['ocr_text']}")
            
    else:
        print(f"Error: The file '{sample_pdf_path}' was not found.")