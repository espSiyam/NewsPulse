from utils.crawler import crawl_news
from utils.database import fetch_crawled_news, insert_crawled_news

SITEMAP_URLS = [
    "https://www.bbc.com/sitemaps/https-sitemap-com-news-1.xml",
    "https://edition.cnn.com/sitemap/news.xml",
    "https://www.foxnews.com/sitemap.xml?type=news",
]

# Database and collection names
DB_NAME = "cognitive_project"
COLLEC_NAME = "news_crawler"

# Crawl news links from the provided sitemap URLs
crawled_news_links = crawl_news(SITEMAP_URLS)

# Fetch existing news entries from the database
existing_news_entries = fetch_crawled_news(DB_NAME, COLLEC_NAME)

# Extract URLs from existing news entries for quick lookup
existing_urls_set = {news_entry["url"] for news_entry in existing_news_entries}

# Filter out news links that are already present in the existing news entries
new_news = [
    news_data
    for news_data in crawled_news_links
    if news_data["url"] not in existing_urls_set
]

# Insert the filtered news links into the database
insertion_status = insert_crawled_news(DB_NAME, COLLEC_NAME, new_news)

print(insertion_status)
