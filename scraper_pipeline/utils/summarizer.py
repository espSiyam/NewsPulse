import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key=os.getenv('GEMINI_KEY')
genai.configure(api_key=openai_api_key)

def summarize_text(input_text, max_tokens=300):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt=f"Write a concise summary of the following text: {input_text} around 100 words"
        response = model.generate_content(prompt, 
                    generation_config = genai.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=1.0
                    )
                )

        return response.text.strip()
    
    except Exception as e:
        raise ValueError(f"Unexpected error during sentiment analysis: {e}")
