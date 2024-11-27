import requests
import tldextract
import xml.etree.ElementTree as ET
import logging
from typing import List, Dict
from utils.constants import cnn_domain_url, bbc_domain_url, foxnews_domain_url
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NAME_SPACE = {
    "ns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "news": "http://www.google.com/schemas/sitemap-news/0.9",
}

SUPPORTED_DOMAINS = {
    "bbc": ["articles", "news", "sport"],
    "cnn": ["video"],
    "foxnews": [],
}


def fetch_sitemap(sitemap_url: str) -> str:
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logger.error(f"Error fetching sitemap: {e}")
        raise


def parse_sitemap(sitemap_url: str) -> List[Dict[str, str]]:
    """
    Parses a sitemap XML from the given URL and extracts relevant information.

    Args:
        sitemap_url (str): The URL of the sitemap to parse.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing parsed sitemap data. Each dictionary contains:
            - 'domain': The domain of the URL.
            - 'category': The category extracted from the URL.
            - 'url': The URL of the sitemap entry.
            - 'publication_date': The publication date of the news entry.
    """
    sitemap_content = fetch_sitemap(sitemap_url)
    root = ET.fromstring(sitemap_content)
    domain = tldextract.extract(sitemap_url).domain

    parsed_sitemap = []
    for url in root.findall("ns:url", NAME_SPACE):
        loc = url.find("ns:loc", NAME_SPACE).text
        news_section = url.find("news:news", NAME_SPACE)
        publication_date = news_section.find("news:publication_date", NAME_SPACE).text
        category = loc.split("/")[3]

        if domain in SUPPORTED_DOMAINS:
            if domain == "cnn" and category in SUPPORTED_DOMAINS[domain]:
                continue
            elif domain != "cnn" and category not in SUPPORTED_DOMAINS[domain]:
                continue
        else:
            logger.warning(f"Unsupported domain: {domain}")
            continue
        
        if domain == "cnn":
            domain_url = cnn_domain_url
        elif domain == "foxnews":
            domain_url = foxnews_domain_url
        elif domain == "bbc":
            domain_url = bbc_domain_url
        else:
            domain_url = None
            
        parsed_sitemap.append(
            {
                "domain": domain,
                "category": category,
                "url": loc,
                "publication_date": publication_date,
                "domain_logo": domain_url,
            }
        )

    return parsed_sitemap


def crawl_news(sitemap_urls: List[str]) -> List[Dict[str, str]]:
    """
    Crawls news articles from a list of sitemap URLs.

    This function takes a list of sitemap URLs, extracts the domain from each URL,
    and checks if the domain is supported. If the domain is supported, it parses
    the sitemap and collects news articles. If the domain is not supported, it logs
    an error and raises a ValueError.

    Args:
        sitemap_urls (List[str]): A list of sitemap URLs to crawl.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing news article data for scraping-
    """
    all_news = []

    for sitemap_url in sitemap_urls:
        domain = tldextract.extract(sitemap_url).domain

        if domain in SUPPORTED_DOMAINS:
            all_news.extend(parse_sitemap(sitemap_url))
        else:
            logger.error(f"Unsupported domain: {domain}")
            raise ValueError(f"Unsupported domain: {domain}")

    return all_news
