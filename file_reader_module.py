import os
import PyPDF2
from groq_module import groq_response
from file_search_module import search_and_open_file

def read_and_respond_to_file(filename):
    # First, search and open the file
    filepath = search_and_open_file(filename)
    if "Could not find" in filepath:
        return filepath

    # Extract the actual filepath from the response message
    filepath = filepath.split("at ")[-1].strip()

    # Read the file content
    _, ext = os.path.splitext(filepath)
    content = None
    if ext.lower() == '.txt':
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return f"Error reading text file: {e}"
    elif ext.lower() == '.pdf':
        try:
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                content = text
        except Exception as e:
            return f"Error reading PDF: {e}"
    else:
        return "File opened, but I can only read text or PDF files."

    if content:
        # Use Groq to generate a response based on the content
        prompt = f"Summarize the following content: {content}"
        response = groq_response(prompt)
        return response
    return "File opened, but no readable content found."