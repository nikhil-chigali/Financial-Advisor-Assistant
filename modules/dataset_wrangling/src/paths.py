"""
This module contains the paths to the data folder and the root folder of the current module.
"""

import os
from pathlib import Path

ROOT_PATH = Path(os.path.dirname(__file__)).parent.resolve()

DATA_PATH = ROOT_PATH / "data"
RAW_NEWS_PATH = DATA_PATH / "raw_news"
