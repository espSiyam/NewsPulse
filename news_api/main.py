from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils.database import fetch_news, fetch_latest_news
import uvicorn

DB_NAME = "cognitive_project"
SCRAPE_COLLECTION = "news_scraper"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/",)
def read_news(limit: int = Query(10, description="Number of news items to fetch")):
    all_news = fetch_news(DB_NAME, SCRAPE_COLLECTION, limit)
    return all_news

@app.get("/latest_news",)
def read_lated_news(limit: int = Query(20, description="Number of news items to fetch")):
    latest_news = fetch_latest_news(DB_NAME, SCRAPE_COLLECTION, limit)
    return latest_news

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  