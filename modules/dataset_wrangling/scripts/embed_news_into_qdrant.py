# DONE: Load JSON news data - scripts
# DONE: Parse each news article and clean the content - src
# DONE: Create `Document` list with cleaned content - src
# DONE: Chunk the cleaned content into small pieces - src
# DONE: Generate embeddings for each chunk - src
# DONE: Authenticate with Qdrant and create a Qdrant Collection - src
# DONE: Push the cleaned content into Qdrant - src

from typing import Dict, List
import os
import sys
import json

from argparse import ArgumentParser
import multiprocessing


from loguru import logger
from tqdm import tqdm


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.paths import RAW_NEWS_PATH
from src.news_documents import parse_article, chunk_document, embed_document
from src.vector_db_api import (
    push_document_to_qdrant,
    get_qdrant_client,
    init_collection,
)

QDRANT_COLLECTION_NAME = "alpaca_news"
VECTOR_SIZE = 384
qdrant_client = get_qdrant_client()
qdrant_client = init_collection(
    qdrant_client,
    QDRANT_COLLECTION_NAME,
    VECTOR_SIZE,
)


def load_news(from_date: str, to_date: str) -> Dict:
    """
    Load news data from a JSON file.

    Args:
    - from_date: str: Start date in the format 'YYYY-MM-DD'.
    - to_date: str: End date in the format 'YYYY-MM-DD'.

    Returns:
    - Dict: News data.
    """
    filename = f"news_{from_date}_{to_date}.json"
    if not os.path.isfile(RAW_NEWS_PATH / filename):
        logger.error(f"News file: {filename} not found!!")
        sys.exit(1)

    with open(RAW_NEWS_PATH / filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def process_and_push_document(
    article: Dict,
) -> None:
    """
    Process and push a news article into Qdrant.

    Args:
    - article: Dict: A news article.

    Returns:
    - None
    """
    # Parsing the doc
    logger.debug("Parsing a new article")
    document = parse_article(article)

    # Chunking the doc
    logger.debug(f"Chunking document {document.id}")
    document = chunk_document(document)

    # Embedding the doc
    logger.debug(f"Embedding document {document.id}")
    document = embed_document(document)

    # Push document to the qdrant collection
    push_document_to_qdrant(document, qdrant_client, QDRANT_COLLECTION_NAME)


def embed_news_into_qdrant(
    news_data: List[Dict],
    num_processes: int,
) -> None:
    """
    Embed news data into Qdrant.

    Args:
    - news_data: List[Dict]: List of news articles.
    - num_processes: int: Number of system processes.

    Returns:
    - None
    """
    logger.info("Number of system processes: {num_processes}")
    if num_processes == 1:
        for doc in news_data:
            process_and_push_document(doc)

    else:
        with multiprocessing.Pool(processes=num_processes) as pool:
            _ = list(
                tqdm(
                    pool.imap(process_and_push_document, news_data),
                    total=len(news_data),
                    desc="Processing",
                    unit="news",
                )
            )


def main(from_date: str, to_date: str, num_processes: int) -> None:
    """
    Main function to embed news data into Qdrant.

    Args:
    - from_date: str: Start date in the format 'YYYY-MM-DD'.
    - to_date: str: End date in the format 'YYYY-MM-DD'.
    - num_processes: int: Number of system processes.

    Returns:
    - None
    """
    data = load_news(from_date, to_date)
    logger.info(f"Number of news articles: {len(data)}")

    logger.info("Processing and embedding news data into Qdrant")
    embed_news_into_qdrant(data, num_processes)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--from_date",
        type=str,
        default="2024-01-01",
        help="Start date in the format 'YYYY-MM-DD'.",
    )
    parser.add_argument(
        "--to_date",
        type=str,
        default="2024-01-30",
        help="End date in the format 'YYYY-MM-DD'.",
    )
    parser.add_argument(
        "--num_processes",
        type=int,
        default=1,
        help="Number of system processes.",
    )
    args = parser.parse_args()

    # Set logger level to INFO
    logger.remove()
    logger.add(sys.stdout, level="INFO")

    main(args.from_date, args.to_date, args.num_processes)
