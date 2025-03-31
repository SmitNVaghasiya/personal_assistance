import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Check if the API key is available
api_key = os.getenv('groq_API')
if not api_key:
    raise ValueError("Groq API key not found. Please set 'groq_API' in your .env file.")

client = Groq(api_key=api_key)

def groq_response(text):
    """
    Sends user input to the Groq API, prepends a prompt, and returns the model's response.
    The prompt instructs the model to answer in short unless the user explicitly asks for detail.
    """
    prompt = '''Answer in short around one to two lines. 
    Provide detail only if explicitly requested and also do not include any codes in response. 
    But you are allowed to give the detailed answer if you think here giving short answer is not enough. Here is the question: '''
    
    full_text = prompt + text
    
    try:
        model_response = client.chat.completions.create(
            messages=[
                {
                    "role": 'user',
                    "content": full_text,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return model_response.choices[0].message.content
    except Exception as e:
        print(f"Error getting Groq response ({type(e).__name__}): {e}")
        return "Sorry, I encountered an error processing your request."