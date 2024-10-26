from typing import List, Optional, Dict
from hashlib import sha256
from unstructured.partition.html import partition_html
from unstructured.cleaners.core import (
    clean_non_ascii_chars,
    replace_unicode_quotes,
    clean,
)
from unstructured.staging.huggingface import chunk_by_attention_window
from transformers import AutoTokenizer, AutoModel
from pydantic import BaseModel
from loguru import logger

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
QDRANT_VECTOR_SIZE = 384


class Document(BaseModel):
    """
    A document object that contains the text, metadata, chunks and embeddings of a news article
    """

    id: str
    text: Optional[List[str]] = []
    metadata: Optional[Dict] = []
    chunks: Optional[List[str]] = []
    embeddings: Optional[List[List[float]]] = []


def parse_article(article: Dict) -> Document:
    """
    Parse the article and clean the content

    Args:
        article (Dict): A dictionary containing the article content, summary, headline and date

    Returns:
        Document: A document object containing the id, cleaned text, and metadata of the article
    """
    # Clean the text
    content = clean(clean_non_ascii_chars(replace_unicode_quotes(article["content"])))
    summary = clean(clean_non_ascii_chars(replace_unicode_quotes(article["summary"])))
    headline = clean(clean_non_ascii_chars(replace_unicode_quotes(article["headline"])))

    # Partition the content
    content = " ".join([str(partition) for partition in partition_html(content)])

    # Create a document object
    doc = Document(
        id=sha256(article["content"].encode()).hexdigest(),
        text=[headline, summary, content],
        metadata={
            "date": article["date"],
            "headline": headline,
            "summary": summary,
        },
    )

    return doc


def chunk_document(document: Document) -> Document:
    """
    Chunk the document into smaller pieces

    Args:
        document (Document): A document object containing the text and metadata of the article

    Returns:
        Document: A document object containing the chunks of the article
    """
    chunks = []
    for text in document.text:
        chunks.extend(
            chunk_by_attention_window(
                text,
                tokenizer,
                max_input_size=QDRANT_VECTOR_SIZE,
            )
        )

    document.chunks = chunks
    return document


def embed_document(document: Document) -> Document:
    """
    Embed the document chunks using a pre-trained transformer model

    Args:
        document (Document): A document object containing the chunks of the article

    Returns:
        Document: A document object containing the embeddings of the chunks
    """
    for chunk in document.chunks:
        tokens = tokenizer(
            chunk,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=QDRANT_VECTOR_SIZE,
        )
        embedding = model(**tokens).last_hidden_state[:, 0, :].detach().cpu().numpy()
        embedding_list = embedding.flatten().tolist()
        document.embeddings.append(embedding_list)

    return document


def process_document(article: Dict) -> List[Document]:
    # Parsing the doc
    logger.debug("Parsing a new article")
    document = parse_article(article)

    # Chunking the doc
    logger.debug(f"Chunking document {document.id}")
    document = chunk_document(document)

    # Embedding the doc
    logger.debug(f"Embedding document {document.id}")
    document = embed_document(document)
