"""
This module contains functions to connect to the qdrant db and initialize a collection.
"""

from typing import Tuple, List

import os
import sys
import hashlib

from dotenv import load_dotenv
from loguru import logger
from hashlib import md5


from qdrant_client import QdrantClient
from qdrant_client.http.api_client import UnexpectedResponse
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.models import PointStruct

from src.utils import Document

load_dotenv()

try:
    QDRANT_API_URL = os.getenv("QDRANT_API_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
except KeyError as e:
    logger.error(f"Error: {e}")
    sys.exit(1)


def get_qdrant_client() -> QdrantClient:
    qdrant_client = QdrantClient(
        url=QDRANT_API_URL,
        api_key=QDRANT_API_KEY,
    )

    return qdrant_client


def init_collection(
    qdrant_client: QdrantClient,
    collection_name: str,
    vector_size: int,
) -> QdrantClient:

    try:
        qdrant_client.get_collection(collection_name=collection_name)
        logger.debug(f"Retrieved an existing Qdrant Collection: {collection_name}")
    except (UnexpectedResponse, ValueError):
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
        logger.debug(f"Re-created Qdrant Collection: {collection_name}")

    return qdrant_client


def build_payloads(doc: Document) -> Tuple[List, List]:
    """
    Build the ids and payloads for each document

    Args:

    Returns:
    """
    ids, payloads = [], []

    for chunk in doc.chunks:
        payload = doc.metadata
        payload.update({"text": chunk})
        chunk_id = hashlib.md5(chunk.encode()).hexdigest()
        ids.append(chunk_id)
        payloads.append(payload)

    return ids, payloads


def push_document_to_qdrant(
    doc: Document, qdrant_client: QdrantClient, collection_name: str
) -> None:
    """ """

    ids, payloads = build_payloads(doc)

    qdrant_client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=idx,
                vector=vector,
                payload=payload,
            )
            for idx, vector, payload in zip(ids, doc.embeddings, payloads)
        ],
    )
