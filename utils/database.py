import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from typing import List, Dict

load_dotenv()
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
uri = f"mongodb+srv://{username}:{password}@cluster0.3rx4l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


def insert_crawled_news(
    db_name: str, collection_name: str, dic_data: List[Dict]
) -> bool:
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            db = client[db_name]
            collection = db[collection_name]
            collection.insert_many(dic_data)
            return True
    except PyMongoError as e:
        raise RuntimeError(f"An error occurred while inserting data: {e}")


def fetch_crawled_news(db_name: str, collection_name: str) -> List[Dict]:
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            collection = client[db_name][collection_name]
            all_documents = list(collection.find())
            return all_documents
    except PyMongoError as e:
        raise RuntimeError(f"An error occurred while fetching data: {e}")


def insert_scraped_news(db_name: str, collection_name: str, news_details: dict) -> bool:
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            db = client[db_name]
            collection = db[collection_name]
            collection.insert_one(news_details)
            return True
    except PyMongoError as e:
        raise RuntimeError(f"An error occurred while inserting data: {e}")


def fetch_scraped_news(db_name: str, collection_name: str) -> List[Dict]:
    try:
        with MongoClient(uri, server_api=ServerApi("1")) as client:
            collection = client[db_name][collection_name]
            all_documents = list(collection.find())
            return all_documents
    except PyMongoError as e:
        raise RuntimeError(f"An error occurred while fetching data: {e}")
