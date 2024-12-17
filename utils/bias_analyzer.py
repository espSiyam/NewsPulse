import google.generativeai as genai

from dotenv import load_dotenv
import os
import json

load_dotenv()

openai_api_key=os.getenv('GEMINI_KEY')
genai.configure(api_key=openai_api_key)

def analyze_bias(input_text):
    try:
        print("Starting the bias analyzer")
        model=genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction='''You are an unbiased news analyst specializing in detecting content bias in news articles. 
                            Analyze the given article for:
                            1. Framing: Identify how the content is framed, including focus on specific aspects while downplaying others.
                            2. Tone: Assess whether the language suggests subtle judgments or biases.
                            3. Selective Details: Highlight significant details included or omitted that may influence the reader's perception.

                            Please return your response **strictly as valid JSON** with the following fields:
                            - "framing": The identified framing in the article.
                            - "tone": The identified tone in the article.
                            - "selective_details": Selective details in the article.
                            - "bias_score": The bias score (1-100).
                            - "bias_level": The bias level (Low, Moderate, High).
                            - "explanation_of_score": Explanation of the score.

                            Make sure the response is valid JSON and does not include any additional text or characters outside the JSON structure.
                            '''
            )
        #Provide detailed insights for each category.
        prompt = (
                f"Analyze this article for bias:\n\n{input_text}"
            )
        print(" Putting into the model to generate")
        response = model.generate_content(prompt)

        #return response.text.strip()
        print("Generated")
        # Debugging: Print the response text to check its contents
        response_text = response.text.strip()
        # Remove the markdown syntax (```json and ```
        if response_text.startswith('```json'):
            response_text = response_text[len('```json'):].strip()
        if response_text.endswith('```'):
            response_text = response_text[:-3].strip()

        #print("Cleaned Response Text: ", repr(response_text))  # Check cleaned output for debugging


        # Check if the response is a valid JSON string
        if len(response_text) > 0:# and response_text.startswith("{") and response_text.endswith("}"):
            # If valid JSON, parse it
            json_response = json.loads(response_text)
            return json_response
        else:
            raise ValueError("Received data is not valid JSON")
    
    except json.JSONDecodeError:
        raise ValueError("The model response is not valid JSON. Check the system instruction and output formatting.")
    
    except Exception as e:
        # Handle unexpected errors
        raise ValueError(f"Unexpected error during bias analysis: {e}")
