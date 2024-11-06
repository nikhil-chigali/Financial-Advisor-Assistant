from typing import Dict, List, Optional
from dataclasses import dataclass
from pydantic import BaseModel
from datetime import datetime


class Document(BaseModel):
    """
    A document object that contains the text, metadata, chunks and embeddings of a news article
    """

    id: str
    text: Optional[List[str]] = []
    metadata: Optional[Dict] = []
    chunks: Optional[List[str]] = []
    embeddings: Optional[List[List[float]]] = []


@dataclass
class News:
    """
    Dataclass for News
    """

    headline: str
    summary: str
    content: str
    date: datetime
