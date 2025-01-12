import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
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

def limit_documents_per_domain(db_name: str, collection_name: str, max_docs: int = 100) -> None:
    """
    Ensures that each domain in the collection has at most `max_docs` documents.
    Deletes the oldest documents if the count exceeds the limit.

    Args:
        db_name (str): The database name.
        collection_name (str): The collection name.
        max_docs (int): The maximum number of documents to retain per domain.
    """
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            db = client[db_name]
            collection = db[collection_name]

            # Get all unique domains
            domains = collection.distinct("domain")
            logging.info(f"Found {len(domains)} domains in the collection.")

            for domain in domains:
                # Count total documents for the domain
                total_docs = collection.count_documents({"domain": domain})

                # Check if we need to delete any documents
                if total_docs > max_docs:
                    excess_docs = total_docs - max_docs
                    logging.info(f"Domain '{domain}' has {total_docs} documents, deleting {excess_docs}.")

                    # Find the oldest documents to delete
                    cursor = collection.find({"domain": domain}).sort("publication_date", ASCENDING).limit(excess_docs)
                    for doc in cursor:
                        collection.delete_one({"_id": doc["_id"]})

            logging.info("Completed pruning excess documents per domain.")
    except PyMongoError as e:
        logging.error(f"An error occurred while limiting documents: {e}")
        raise RuntimeError(f"An error occurred while limiting documents: {e}")


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