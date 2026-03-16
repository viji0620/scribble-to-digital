import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

from image_processing import preprocess_image
from ocr_module import extract_text
from ai_processor import setup_gemini, process_text, parse_ai_output
from export_utils import create_download_text

# Page configuration
st.set_page_config(
    page_title="Scribble to Digital",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for magenta and white theme
st.markdown("""
    <style>
        :root {
            --primary: #C2185B;
            --secondary: #FFFFFF;
            --dark: #121212;
        }
        
        body {
            background-color: #F5F5F5;
        }
        
        .main {
            padding: 2rem;
        }
        
        .title-section {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #C2185B 0%, #A01347 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(194, 24, 91, 0.2);
        }
        
        .title-section h1 {
            font-size: 3rem;
            margin: 0;
            font-weight: 800;
            letter-spacing: -1px;
        }
        
        .title-section p {
            font-size: 1.1rem;
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
        }
        
        .section-header {
            display: flex;
            align-items: center;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 3px solid #C2185B;
        }
        
        .section-header h2 {
            margin: 0;
            color: #C2185B;
            font-weight: 700;
        }
        
        .step-badge {
            display: inline-block;
            background-color: #C2185B;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
            margin-right: 1rem;
        }
        
        .success-box {
            background-color: #F3E5F5;
            border-left: 5px solid #C2185B;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .info-box {
            background-color: #F8BBD0;
            border-left: 5px solid #C2185B;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            color: #7B1D42;
        }
        
        .process-button {
            background: linear-gradient(135deg, #C2185B 0%, #A01347 100%);
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(194, 24, 91, 0.3);
        }
        
        .process-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(194, 24, 91, 0.4);
        }
        
        .task-item {
            background-color: #FFFFFF;
            border-left: 4px solid #C2185B;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 4px;
            font-weight: 500;
        }
        
        .download-button {
            background: linear-gradient(135deg, #C2185B 0%, #A01347 100%);
            color: white;
        }
        
        .instruction-section {
            background: linear-gradient(135deg, #F3E5F5 0%, #F8BBD0 100%);
            border: 2px solid #C2185B;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
        }
        
        .instruction-section h3 {
            color: #C2185B;
            margin-top: 0;
        }
        
        .instruction-item {
            color: #424242;
            margin: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }
        
        .instruction-item:before {
            content: "→";
            position: absolute;
            left: 0;
            color: #C2185B;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'image_processed' not in st.session_state:
    st.session_state.image_processed = False
if 'ocr_extracted' not in st.session_state:
    st.session_state.ocr_extracted = False
if 'ai_processed' not in st.session_state:
    st.session_state.ai_processed = False
if 'ocr_text' not in st.session_state:
    st.session_state.ocr_text = ""
if 'corrected_text' not in st.session_state:
    st.session_state.corrected_text = ""
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []

# Title Section
st.markdown("""
    <div class="title-section">
        <h1>✍️ Scribble to Digital</h1>
        <p>Transform your handwritten notes into structured digital text</p>
    </div>
""", unsafe_allow_html=True)

# Instructions Section
st.markdown("""
    <div class="instruction-section">
        <h3>📋 How to Use</h3>
        <div class="instruction-item"><strong>Step 1:</strong> Upload a clear image of your handwritten notes</div>
        <div class="instruction-item"><strong>Step 2:</strong> Click the "Process Image" button</div>
        <div class="instruction-item"><strong>Step 3:</strong> Review the raw OCR text</div>
        <div class="instruction-item"><strong>Step 4:</strong> See AI-corrected text and extracted tasks</div>
        <div class="instruction-item"><strong>Step 5:</strong> Download your results as a text file</div>
    </div>
""", unsafe_allow_html=True)

# File uploader section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header"><span class="step-badge">STEP 1</span><h2>Upload Image</h2></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose an image file of your handwritten notes",
        type=["png", "jpg", "jpeg"],
        help="Supported formats: PNG, JPG, JPEG. For best results, ensure good lighting and clear handwriting."
    )

with col2:
    if uploaded_file is not None:
        st.success("✅ Image uploaded successfully!")
    else:
        st.info("📁 Waiting for image upload...")

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.markdown('<div style="border: 2px solid #E91E63; border-radius: 12px; padding: 1rem; margin: 1rem 0;">', unsafe_allow_html=True)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process button
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        process_button = st.button(
            "🚀 Process Image",
            key="process_btn",
            use_container_width=True
        )
    
    if process_button:
        st.session_state.image_processed = False
        st.session_state.ocr_extracted = False
        st.session_state.ai_processed = False
        
        with st.spinner("🔄 Processing your image..."):
            try:
                # Convert PIL image to OpenCV format
                image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Preprocess the image
                processed_image = preprocess_image(image_cv)
                st.session_state.image_processed = True
                
                # Extract raw OCR text
                ocr_text = extract_text(processed_image)
                st.session_state.ocr_text = ocr_text
                st.session_state.ocr_extracted = True
                
                # Check for API key
                api_key = os.getenv("GOOGLE_API_KEY")
                if not api_key:
                    st.error("❌ Please set the GOOGLE_API_KEY environment variable.")
                else:
                    # Set up Gemini client
                    client = setup_gemini(api_key)
                    
                    # Process text with AI
                    ai_output = process_text(client, ocr_text)
                    
                    # Parse the output
                    corrected_text, todo_list = parse_ai_output(ai_output)
                    st.session_state.corrected_text = corrected_text
                    st.session_state.todo_list = todo_list
                    st.session_state.ai_processed = True
                    
            except Exception as e:
                st.error(f"❌ Error processing image: {str(e)}")
    
    # Display results progressively
    if st.session_state.image_processed:
        st.markdown("""
            <div class="success-box">
                ✅ <strong>Image preprocessing complete</strong> - Image has been enhanced for better OCR accuracy
            </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.ocr_extracted:
        st.markdown('<div class="section-header"><span class="step-badge">STEP 2</span><h2>Raw OCR Text</h2></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="success-box">
                ✅ <strong>OCR extraction complete</strong> - Text has been extracted from your image
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📄 View Raw OCR Text", expanded=True):
            st.text_area(
                "Raw Text",
                st.session_state.ocr_text,
                height=150,
                disabled=True,
                key="raw_ocr"
            )
    
    if st.session_state.ai_processed:
        st.markdown('<div class="section-header"><span class="step-badge">STEP 3</span><h2>AI Corrected Text</h2></div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="success-box">
                ✅ <strong>AI processing complete</strong> - Text has been corrected and tasks have been extracted
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📝 View Corrected Text", expanded=True):
            st.text_area(
                "Corrected Text",
                st.session_state.corrected_text,
                height=200,
                disabled=True,
                key="corrected"
            )
        
        # To-Do List section
        st.markdown('<div class="section-header"><span class="step-badge">STEP 4</span><h2>Extracted To-Do List</h2></div>', unsafe_allow_html=True)
        
        if st.session_state.todo_list:
            st.markdown("""
                <div class="success-box">
                    ✅ <strong>Task extraction successful</strong> - Found the following tasks in your notes
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("✓ View Tasks", expanded=True):
                for idx, task in enumerate(st.session_state.todo_list, 1):
                    st.markdown(f'<div class="task-item">• {task}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="info-box">
                    ℹ️ No specific tasks were found in your notes. The corrected text has been prepared for download.
                </div>
            """, unsafe_allow_html=True)
        
        # Download section
        st.markdown('<div class="section-header"><span class="step-badge">STEP 5</span><h2>Download Results</h2></div>', unsafe_allow_html=True)
        
        download_content = create_download_text(st.session_state.corrected_text, st.session_state.todo_list)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="⬇️ Download Results as TXT",
                data=download_content,
                file_name="scribble_to_digital_result.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_btn"
            )
        
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem; color: #666; font-size: 0.9rem;">
                💡 <strong>Tip:</strong> You can upload another image to process more notes
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="info-box" style="text-align: center; margin-top: 3rem;">
            <h3 style="margin-top: 0;">👆 Start by uploading an image</h3>
            <p>Upload a clear photo or scan of your handwritten notes to begin the transformation process.</p>
        </div>
    """, unsafe_allow_html=True)