
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from typing import List, Dict
import logging


load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
uri = f"mongodb+srv://{username}:{password}@cluster0.3rx4l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def fetch_news(db_name: str, collection_name: str, limit: int) -> List[Dict]:
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            collection = client[db_name][collection_name]
            all_documents = list(
                collection.find({},{"_id": 0,
                                    "title": 1, 
                                    "text": 1, 
                                    "main_image": 1, 
                                    "domain": 1, 
                                    "category": 1, 
                                    }).limit(limit))
            return all_documents
    except PyMongoError as e:
        logging.error(f"An error occurred while fetching data: {e}")
        raise RuntimeError(f"An error occurred while fetching data: {e}")
