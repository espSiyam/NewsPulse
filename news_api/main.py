from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils.database import fetch_news
import uvicorn

DB_NAME = "cognitive_project"
SCRAPE_COLLECTION = "news_scraper"
LIMIT = 10

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/",)
def read_root():
    all_news = fetch_news(DB_NAME, SCRAPE_COLLECTION, LIMIT)
    return all_news

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  