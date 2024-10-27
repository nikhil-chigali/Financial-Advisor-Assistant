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
from functools import partial


from loguru import logger
from tqdm import tqdm
from qdrant_client import QdrantClient

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


def load_news(from_date: str, to_date: str) -> Dict:

    filename = f"news_{from_date}_{to_date}.json"
    if not os.path.isfile(RAW_NEWS_PATH / filename):
        logger.error(f"News file: {filename} not found!!")
        sys.exit(1)

    with open(RAW_NEWS_PATH / filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def process_and_push_document(
    qdrant_client: QdrantClient,
    collection_name: str,
    article: Dict,
) -> None:
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
    push_document_to_qdrant(document, qdrant_client, collection_name)


def embed_news_into_qdrant(
    news_data: List[Dict],
    qdrant_client: QdrantClient,
    collection_name: str,
    num_processes: int,
) -> None:

    if num_processes == 1:
        for doc in news_data:
            process_and_push_document(qdrant_client, collection_name, doc)

    else:

        # Parallel Processing.
        import multiprocessing

        # Create a partial function to ensure that all the data is loaded in the same collection of the qdrant client.
        process_and_push_document_partial = partial(
            process_and_push_document,
            qdrant_client,
            collection_name,
        )
        with multiprocessing.Pool(processes=num_processes) as pool:
            tqdm(
                pool.imap(process_and_push_document_partial, news_data),
                total=len(news_data),
                desc="Processing",
                unit="news",
            )


def main(from_date: str, to_date: str, num_processes: int) -> None:
    data = load_news(from_date, to_date)

    qdrant_client = get_qdrant_client()
    qdrant_client = init_collection(
        qdrant_client,
        QDRANT_COLLECTION_NAME,
        VECTOR_SIZE,
    )

    embed_news_into_qdrant(data, qdrant_client, QDRANT_COLLECTION_NAME, num_processes)


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
        default="2024-01-09",
        help="End date in the format 'YYYY-MM-DD'.",
    )
    parser.add_argument(
        "--num_processes",
        type=int,
        default=1,
        help="Number of system processes.",
    )
    args = parser.parse_args()

    main(args.from_date, args.to_date, args.num_processes)
