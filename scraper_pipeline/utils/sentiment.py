import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key=os.getenv('GEMINI_KEY')
genai.configure(api_key=openai_api_key)

def analyze_sentiment(input_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # prompt = f"Analyze the sentiment of the following text and respond with 'Positive', 'Negative', or 'Neutral' along with a score from -1 to 1, where -1 is very negative, 0 is neutral, and 1 is very positive:\n\n{input_text}"
        prompt = (
                f"Analyze the sentiment of the following text and respond with only the sentiment score, "
                f"where -1 represents negative, 0 represents neutral, and 1 represents positive:\n\n{input_text},"
                f"Do not include any text or explanations, only output the numerical score."
            )
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        # Handle unexpected errors
        raise ValueError(f"Unexpected error during sentiment analysis: {e}")
