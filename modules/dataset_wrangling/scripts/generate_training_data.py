"""
    This script contains the functions to generate training data from one of the following large-language models:
    ["openai/gpt-4o", "openai/gpt-4o-mini", "openai/gpt-3.5-turbo"]
"""

from typing import Dict, List
from argparse import ArgumentParser

import os
import sys
import json
import dspy


from tqdm import tqdm
from loguru import logger
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.paths import ROOT_PATH, DATA_PATH
from src.data_gen import GenerateSuggestions


def configure_dspy(model_name: str) -> None:
    """
    This function takes configures the large-language model which we would like to use.

    Args:
        model_name (str): User's desired choice of LLM.

    Returns:
        None
    """
    load_dotenv()
    try:
        if "OPENAI_API_KEY" not in os.environ:
            raise KeyError("API Key is not available")
    except KeyError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

    logger.info(f"Setting DSPY LM: {model_name}")
    lm = dspy.LM(model_name)
    dspy.configure(lm=lm)


def generate_data(examples: List[Dict]) -> List[Dict]:
    """
    This function takes in the sample data we have to generate training data.

    Args:
        examples (List[Dict]): A list of dicts {
            about_me (str): User's Information and Query.
            context (str): Relevant factoid for answering the Query.
        }

    Return:
        data (List[Dict]): A list of dicts {
            about_me (str): User's Information and Query.
            context (str): Relevant factoid for answering the Query.
            answer (str): Reasoning and resposne for the query based on the input.
        }
    """
    lm_module = GenerateSuggestions()

    logger.info("Generating responses for the examples")
    data = []
    for i, example in tqdm(
        enumerate(examples), desc="Generating response", total=len(examples)
    ):
        output = lm_module(**example)

        example["answer"] = output.response

        data.append(example)

    return data


def load_examples() -> Dict:
    """
    Loads examples from a JSON file located at the specified DATA_PATH.

    This function reads a JSON file named "examples.json" from the predefined
    DATA_PATH and returns the data as a dictionary. It logs the path from which
    the data is being loaded, as well as the number of examples successfully loaded.

    Returns:
        Dict: A dictionary containing the examples loaded from the JSON file.
    """

    logger.info(f"Loading the Examples from Path - {DATA_PATH / 'exmaples.json'}")
    with open(DATA_PATH / "examples.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    logger.info(f"Successfully loaded {len(data)} examples.")
    return data


def main(model_name: str) -> None:
    """
    Main function to configure, generate, and save training data.

    This function performs the following tasks:
    1. Configures the environment or settings required for data processing based on the provided model name.
    2. Loads examples from a predefined JSON file.
    3. Generates data based on the loaded examples.
    4. Saves the generated data to a "training_data.json" file at the specified DATA_PATH.

    Args:
        model_name (str): The name of the model to configure for data processing.

    Returns:
        None
    """
    configure_dspy(model_name)

    examples = load_examples()

    data = generate_data(examples)
    logger.info(f"Saving {len(data)} examples to {DATA_PATH / 'training_data.json'}")
    with open(DATA_PATH / "training_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        default="openai/gpt-4o-mini",
        choices=["openai/gpt-4o", "openai/gpt-4o-mini", "openai/gpt-3.5-turbo"],
    )
    args = parser.parse_args()

    main(args.model)
