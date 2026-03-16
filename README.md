# Scribble to Digital

## Project Overview
Scribble to Digital is a Streamlit web application that converts handwritten notes into structured digital text and extracts To-Do tasks using OCR and Google Gemini AI.

## Features
- Upload images of handwritten notes
- Preprocess images for better OCR accuracy
- Extract raw text using OCR
- Correct and improve text using Google Gemini AI
- Extract actionable To-Do tasks
- Display raw OCR text, corrected text, and To-Do list
- Download results as a TXT file

## Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **Libraries:** streamlit, opencv-python, pytesseract, pillow, google-generativeai

## Installation Steps
1. Clone the repository or download the project files.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install Tesseract OCR:
   - On Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
   - On macOS: `brew install tesseract`
   - On Windows: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
4. Set up Google Gemini API:
   - Obtain an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set the environment variable: `export GOOGLE_API_KEY=your_api_key_here`

## How to Run
1. Navigate to the project directory:
   ```
   cd scribble-to-digital
   ```
2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
3. Open the provided URL in your browser.

## Example Output
After uploading an image and processing:
- **Raw OCR Text:** Raw extracted text from the image.
- **Corrected Text:** Grammar and spelling corrected, formatted text.
- **Todo List:** List of extracted tasks.
- Download button to save the results as a TXT file.