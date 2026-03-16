import pytesseract

# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image):
    """
    Extract raw text from the preprocessed image using pytesseract.
    """

    # Better OCR configuration
    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(image, config=custom_config)

    return text.strip()