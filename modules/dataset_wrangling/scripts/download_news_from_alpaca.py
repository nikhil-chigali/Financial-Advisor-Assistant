"""
This script downloads news data from Alpaca API.

Usage:
    python download_news_from_alpaca.py --from_date "2024-10-01" --to_date "2024-10-25"
    
Arguments:
    --from_date (str): Start date in the format "YYYY-MM-DD".
    --to_date (str): End date in the format "YYYY-MM-DD".
"""

import os
import sys
from argparse import ArgumentParser
from loguru import logger
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.alpaca_api import download_historical_news


def main(from_date: str, to_date: str) -> None:
    """
    Download news data from Alpaca API.

    Args:
        from_date (str): Start date in the format "YYYY-MM-DD".
        to_date (str): End date in the format "YYYY-MM-DD".
    """
    from_date = datetime.fromisoformat(from_date)
    to_date = datetime.fromisoformat(to_date)

    filename = download_historical_news(
        from_date=from_date,
        to_date=to_date,
    )
    logger.info(f"News data downloaded from Alpaca and saved at: {filename}")


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
        default="2024-01-31",
        help="End date in the format 'YYYY-MM-DD'.",
    )
    args = parser.parse_args()

    logger.add(
        "logs/detailed_logs.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}",
        rotation="50 MB",
        retention="20 days",
        level="DEBUG",
    )

    main(args.from_date, args.to_date)
