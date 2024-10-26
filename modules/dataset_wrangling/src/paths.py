"""
    This script stores all the paths that are used in the dataset_wrangling module.
"""

import os
from pathlib import Path

ROOT_PATH = Path(os.path.dirname(__file__)).parent.resolve()

DATA_PATH = ROOT_PATH / "data"
