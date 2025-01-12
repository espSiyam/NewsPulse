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
        if not isinstance(search_vector, list) or not all(isinstance(x, (int, float)) for x in search_vector):
            raise ValueError(f"Invalid search vector type for document {doc_id}: {search_vector}")

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
                },
                {
                    "$project": {
                        "_id": 1,
                        "title": 1,
                        "url": 1,
                        "main_image": 1
                    }
                }
            ])
            similar_docs = list(result)
            similar_docs = [doc for doc in similar_docs if doc['_id'] != doc_id]
            
            return similar_docs[:5]
    except PyMongoError as e:
        logging.error(f"An error occurred while finding similar documents: {e}")
        raise RuntimeError(f"An error occurred while finding similar documents: {e}")
    except ValueError as e:
        logging.error(e)
        raise RuntimeError(e)

def find_sim_news(db_name: str, collection_name: str):
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            db = client[db_name]
            collection = db[collection_name]
            documents = list(collection.find())

            for doc in documents:
                try:
                    logging.info(f"Searching for similar documents for: {doc['_id']}")
                    search_vector = doc.get('embedding', [])
                    if not search_vector:
                        logging.warning(f"Skipping document {doc['_id']} due to empty embedding")
                        continue

                    similar_docs = find_top_5_similar_docs(db_name, collection_name, search_vector, doc['_id'])
                    collection.update_one(
                        {"_id": doc["_id"]}, {"$set": {"top_5_similar": similar_docs}}
                    )
                except Exception as e:
                    logging.error(f"An error occurred while processing document {doc['_id']}: {e}")
                    continue  # Continue with the next document

            logging.info(f"All documents updated with top 5 similar document details in {db_name}.{collection_name}")
    except PyMongoError as e:
        logging.error(f"An error occurred while updating data: {e}")
        raise RuntimeError(f"An error occurred while updating data: {e}")