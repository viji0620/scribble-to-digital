import google.genai as genai

def setup_gemini(api_key):
    """
    Configure and return the Google Gemini client.
    """
    client = genai.Client(api_key=api_key)
    return client

def process_text(client, ocr_text):
    """
    Send OCR text to Gemini AI for correction and task extraction.
    """
    prompt = """You are an assistant that cleans handwritten notes.

Tasks:
1. Fix spelling mistakes
2. Improve grammar
3. Reconstruct broken words
4. Format text into readable paragraphs
5. Extract actionable tasks

Return output in this format:

Corrected Text:
<text>

Todo List:
- task1
- task2
- task3

"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt + ocr_text
    )
    return response.text

def parse_ai_output(ai_output):
    """
    Parse the AI output to extract corrected text and todo list.
    Assumes the output follows the specified format.
    """
    lines = ai_output.strip().split('\n')
    corrected_text = ""
    todo_list = []
    
    in_corrected = False
    in_todo = False
    
    for line in lines:
        if line.startswith("Corrected Text:"):
            in_corrected = True
            in_todo = False
            continue
        elif line.startswith("Todo List:"):
            in_corrected = False
            in_todo = True
            continue
        
        if in_corrected:
            corrected_text += line + "\n"
        elif in_todo and line.strip().startswith("-"):
            todo_list.append(line.strip()[1:].strip())
    
    return corrected_text.strip(), todo_list