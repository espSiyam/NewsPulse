import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key=os.getenv('GEMINI_KEY')
genai.configure(api_key=openai_api_key)

def classify_text(input_text, max_tokens=300):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt=f"Classify the following text into one of the categories: Politics, Business, Technology, Sports, Health, Science, Entertainment, World News, Environment, Crime, Education, Lifestyle, Travel, Culture, Opinion/Editorial. The text is:{input_text} . Just give the category, no other text."
        
        response = model.generate_content(prompt, 
                    generation_config = genai.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=1.0
                    )
                )

        return response.text.strip()
    
    except Exception as e:
        raise ValueError(f"Unexpected error during sentiment analysis: {e}")
