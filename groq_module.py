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

def groq_response(text, intent_recognition=False):
    """
    Sends user input to the Groq API, prepends a prompt, and returns the model's response.
    The prompt instructs the model to answer in short unless the user explicitly asks for detail.
    Handles rate limits by switching models if necessary.
    If intent_recognition is True, the prompt is adjusted to classify the intent.
    """
    if intent_recognition:
        prompt = '''Classify the intent of the following user input into one of these categories: 
        list_tasks, mark_task, general_query. Return only the category name. Here is the input: '''
    else:
        prompt = '''Answer in short around one to two lines. 
        Provide detail only if explicitly requested and also do not include any codes in response. 
        But you are allowed to give the detailed answer if you think here giving short answer is not enough. Here is the question: '''

    full_text = prompt + text

    # Try the primary model first
    try:
        model_response = client.chat.completions.create(
            messages=[
                {
                    "role": 'user',
                    "content": full_text,
                }
            ],
            model="llama3-8b-8192",  # Smaller model for faster response
        )
        return model_response.choices[0].message.content

    except Exception as e:
        if "rate limit" in str(e).lower():
            print("Rate limit exceeded for LLaMA model, switching to DeepSeek...")
            try:
                model_response = client.chat.completions.create(
                    messages=[
                        {
                            "role": 'user',
                            "content": full_text,
                        }
                    ],
                    model="deepseek-coder-v2-lite-instruct",  # Fallback model
                )
                return model_response.choices[0].message.content
            except Exception as e2:
                print(f"Error with DeepSeek model ({type(e2).__name__}): {e2}")
                return "Sorry, I encountered an error due to rate limits."
        else:
            print(f"Error getting Groq response ({type(e).__name__}): {e}")
            return "Sorry, I encountered an error processing your request."