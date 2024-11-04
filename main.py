from utils.database import fetch_crawled_news
from utils.scraper import scrape_and_insert_news

DB_NAME = "cognitive_project"
CRAWL_COLLECTION = "news_crawler"
SCRAPE_COLLECTION = "news_scraper"

crawled_news_collec = fetch_crawled_news(DB_NAME, CRAWL_COLLECTION)

scrape_and_insert_news(crawled_news_collec, DB_NAME, SCRAPE_COLLECTION)
