import os
import logging
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
uri = f"mongodb+srv://{username}:{password}@cluster0.3rx4l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def insert_crawled_news(db_name: str, collection_name: str, dic_data: List[Dict]) -> bool:
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            db = client[db_name]
            collection = db[collection_name]
            collection.insert_many(dic_data)
            logging.info(f"Inserted {len(dic_data)} documents into {db_name}.{collection_name}")
            return True
    except PyMongoError as e:
        logging.error(f"An error occurred while inserting data: {e}")
        raise RuntimeError(f"An error occurred while inserting data: {e}")

def fetch_crawled_news(db_name: str, collection_name: str) -> List[Dict]:
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            collection = client[db_name][collection_name]
            all_documents = list(collection.find())
            logging.info(f"Fetched {len(all_documents)} documents from {db_name}.{collection_name}")
            return all_documents
    except PyMongoError as e:
        logging.error(f"An error occurred while fetching data: {e}")
        raise RuntimeError(f"An error occurred while fetching data: {e}")

def insert_scraped_news(db_name: str, collection_name: str, news_details: dict) -> bool:
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            db = client[db_name]
            collection = db[collection_name]
            collection.insert_one(news_details)
            logging.info(f"Inserted document into {db_name}.{collection_name}")
            return True
    except PyMongoError as e:
        logging.error(f"An error occurred while inserting data: {e}")
        raise RuntimeError(f"An error occurred while inserting data: {e}")

def fetch_scraped_news(db_name: str, collection_name: str) -> List[Dict]:
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            collection = client[db_name][collection_name]
            all_documents = list(collection.find())
            logging.info(f"Fetched {len(all_documents)} documents from {db_name}.{collection_name}")
            return all_documents
    except PyMongoError as e:
        logging.error(f"An error occurred while fetching data: {e}")
        raise RuntimeError(f"An error occurred while fetching data: {e}")

def find_top_5_similar_docs(db_name: str, collection_name: str, search_vector, doc_id):
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            db = client[db_name]
            result = db[collection_name].aggregate([
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding",
                        "queryVector": search_vector,
                        "numCandidates": 100,
                        "limit": 6
                    }
                }
            ])
            similar_docs = list(result)
            similar_docs = [doc for doc in similar_docs if doc['_id'] != doc_id]
            return similar_docs[:5]
    except PyMongoError as e:
        logging.error(f"An error occurred while finding similar documents: {e}")
        raise RuntimeError(f"An error occurred while finding similar documents: {e}")

def find_sim_news(db_name: str, collection_name: str):
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            db = client[db_name]
            collection = db[collection_name]
            documents = list(collection.find())

            for doc in documents:
                try:
                    logging.info(f"Searching for similar documents for: {doc['_id']}")
                    search_vector = doc['embedding']
                    similar_docs = find_top_5_similar_docs(db_name, collection_name, search_vector, doc['_id'])
                    top_5_similar_ids = [similar_doc['_id'] for similar_doc in similar_docs]
                    collection.update_one(
                        {"_id": doc["_id"]}, {"$set": {"top_5_similar": top_5_similar_ids}}
                    )
                except Exception as e:
                    logging.error(f"An error occurred while processing document {doc['_id']}: {e}")
                    continue 

            logging.info(f"All documents updated with top 5 similar document IDs in {db_name}.{collection_name}")
    except PyMongoError as e:
        logging.error(f"An error occurred while updating data: {e}")
        raise RuntimeError(f"An error occurred while updating data: {e}")