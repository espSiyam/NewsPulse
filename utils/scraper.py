import time
import random
import requests
from newspaper import Article
from datetime import datetime
import tldextract
from fake_useragent import UserAgent
import logging
from typing import List, Dict
from .database import insert_scraped_news, fetch_scraped_news
from utils.embedding import generate_embedding

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ua = UserAgent()


def scrape_article(url: str) -> Dict[str, str]:
    headers = {"User-Agent": ua.random}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch the URL: {url} - {e}")
        raise

    # Download and parse the article
    article = Article(url)
    article.download(input_html=response.text)
    article.parse()

    # Extract details
    scrape_date = datetime.today().strftime("%Y-%m-%d")
    title = article.title
    text = article.text
    embedding = generate_embedding(title, text)
    main_image = article.top_image

    # Sleep for a random duration to avoid being blocked
    time.sleep(random.uniform(1, 5))

    logger.info(f"Finished scraping the URL: {url}")

    return {
        "status": "success",
        "current_date": scrape_date,
        "title": title,
        "text": text,
        "embedding": embedding,
        "main_image": main_image,
    }


def scrape_and_insert_news(
    news_to_scrape: List[Dict[str, str]], db_name: str, collection_name: str
) -> None:
    scraped_news = fetch_scraped_news(db_name, collection_name)
    existing_urls_set = {news["url"] for news in scraped_news}
    new_news_to_scrape = [
        news_data
        for news_data in news_to_scrape
        if news_data["url"] not in existing_urls_set
    ]

    for news_info in new_news_to_scrape:
        url = news_info["url"]
        logger.info(f"Processing URL: {url}")
        try:
            scraped_data = scrape_article(url)
            scraped_data.update(news_info)
            insert_scraped_news(db_name, collection_name, scraped_data)
        except requests.RequestException as e:
            logger.error(f"Request error scraping {url}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
