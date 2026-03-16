import cv2

def preprocess_image(image):
    """
    Preprocess the uploaded image for better OCR accuracy.
    - Convert to grayscale
    - Apply noise reduction
    - Apply thresholding
    Returns the enhanced image.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Noise reduction using Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh