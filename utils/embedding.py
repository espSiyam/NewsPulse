import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from utils.constants import EMBEDDING_MODEL, RETRIVAL_TASK

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_embedding(title, text):
    """
    Generates embeddings for the given title and text.
    Args:
        title (str): The title of the content to generate embeddings for.
        text (str): The text content to generate embeddings for.
    Returns:
        embedding: The generated embeddings if successful, None otherwise.
    Raises:
        ValueError: If the API key is not found in the environment variables.
        Exception: If any other error occurs during the embedding generation process.
    """
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables")
        
        genai.configure(api_key=api_key)
        logging.info("Generating embeddings...")
        embedding_response = genai.embed_content(
            model=EMBEDDING_MODEL,
            title=title,
            content=text,
            task_type=RETRIVAL_TASK,
        )
        logging.info("Embeddings generated successfully")
        embedding = embedding_response["embedding"]
        return embedding

    except Exception as e:
        logging.error("An error occurred while generating embeddings: %s", e)
        return None