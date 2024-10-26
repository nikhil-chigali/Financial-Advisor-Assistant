"""
This module contains functions to fetch news articles from the Alpaca API and save them to a JSON file.
"""

from typing import Tuple, List
import os
import sys
from pathlib import Path

import html
import re
import json
from dataclasses import dataclass
from datetime import datetime
import requests
from loguru import logger
from dotenv import load_dotenv

from src.paths import DATA_PATH

load_dotenv()

try:
    APCA_API_KEY_ID = os.environ["APCA_API_KEY_ID"]
    APCA_API_SECRET_KEY = os.environ["APCA_API_SECRET_KEY"]
except KeyError as e:
    logger.error(f"Error: {e}")
    sys.exit(1)


@dataclass
class News:
    """
    Dataclass for News
    """

    headline: str
    summary: str
    content: str
    date: datetime


def clean_text(content: str) -> str:
    """
    Cleans the content of the news articles by removing special characters, stopwords, html tags and blank spaces

    Args:
        content (str): The content of the news article

    Returns:
        str: The cleaned content of the news article
    """
    # Remove HTML entities
    clean_content = html.unescape(content)

    # Remove HTML tags
    clean_content = re.sub(r"<[^>]*>", "", clean_content)

    # Remove spaces and newlines
    clean_content = re.sub(r"\s+", " ", clean_content)

    return clean_content


def fetch_news_batch(
    from_date: datetime, to_date: datetime, next_page_token: str = None
) -> Tuple[List[News], str]:
    """
    Fetch news in batches from Alpaca API using the provided date range

    Args:
        from_date (datetime): The start date
        to_date (datetime): The end date
        next_page_token (str): The next page token

    Returns:
        Tuple[News, str]: A tuple containing the list of news articles and the next page token
    """
    # Alpaca API URL
    url = "https://data.alpaca.markets/v1beta1/news"

    # Alpaca API headers and parameters
    header = {
        "APCA-API-KEY-ID": APCA_API_KEY_ID,
        "APCA-API-SECRET-KEY": APCA_API_SECRET_KEY,
    }
    params = {
        "start": from_date.strftime("%Y-%m-%d"),
        "end": to_date.strftime("%Y-%m-%d"),
        "sort": "asc",
        "limit": 50,
        "include_content": "true",
        "exclude_contentless": "false",
    }

    # Add next page token if available
    if next_page_token:
        params["page_token"] = next_page_token

    # Fetch news from Alpaca API
    response = requests.get(url, headers=header, params=params, timeout=10)

    # Check if the response is successful
    if response.status_code != 200:
        logger.error(f"Error: {response.status_code}")
        sys.exit(1)

    # Parse the response JSON
    data = response.json()
    next_page_token = data.get("next_page_token", None)

    # Extract news articles from the response
    news_batch = []
    for news in data["news"]:
        headline = clean_text(news["headline"])
        summary = clean_text(news["summary"])
        content = clean_text(news["content"])
        date = datetime.fromisoformat(news["updated_at"])

        news_batch.append(News(headline, summary, content, date))

    return news_batch, next_page_token


def save_news_to_json(news: List[News]) -> Path:
    """
    Save news to JSON file in the `data` directory

    Args:
        list_of_news (List[News]): A list of news articles

    Returns:
        Path: The path to the saved JSON file
    """
    # Get the start and end date of the news articles
    from_date = news[0].date.strftime("%Y-%m-%d")
    to_date = news[-1].date.strftime("%Y-%m-%d")
    filename = DATA_PATH / "news" / f"news_{from_date}_{to_date}.json"

    # Save the news to a JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            [
                {
                    "headline": news_article.headline,
                    "summary": news_article.summary,
                    "content": news_article.content,
                    "date": news_article.date.isoformat(),
                }
                for news_article in news
            ],
            f,
            ensure_ascii=False,
            indent=4,
        )

    return filename


def download_historical_news(from_date: datetime, to_date: datetime) -> Path:
    """
    Download news from Alpaca API and save to a JSON file in the `data` directory

    Args:
        from_date (datetime): The start date
        to_date (datetime): The end date

    Returns:
        Path: The path to the saved JSON file
    """
    # Fetch news from Alpaca API
    logger.info("Downloading news from Alpaca API...")
    logger.info(f"From: {from_date} to {to_date}")
    news_batch, next_page_token = fetch_news_batch(from_date, to_date)
    list_of_news = news_batch

    # Fetch news in batches until there are no more news articles
    while next_page_token:
        logger.debug(
            f"Downloaded {len(news_batch)} news articles with last date {news_batch[-1].date}"
        )
        news_batch, next_page_token = fetch_news_batch(
            from_date, to_date, next_page_token
        )
        list_of_news += news_batch

    logger.info(
        f"Downloaded {len(list_of_news)} news articles between {from_date} and {to_date}"
    )

    # Save news to JSON file
    logger.info("Saving news to JSON")
    filename = save_news_to_json(list_of_news)
    logger.info(f"News saved to {filename}")

    return filename
