from utils.database import fetch_crawled_news, find_sim_news
from utils.scraper import scrape_and_insert_news
from utils.constants import DB_NAME, CRAWL_COLLECTION, SCRAPE_COLLECTION

# crawled_news_collec = fetch_crawled_news(DB_NAME, CRAWL_COLLECTION)

# scrape_and_insert_news(crawled_news_collec, DB_NAME, SCRAPE_COLLECTION)

find_sim_news(DB_NAME, SCRAPE_COLLECTION)
