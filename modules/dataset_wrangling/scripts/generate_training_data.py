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

    load_dotenv()
    if "OPENAI_API_KEY" in os.environ:
        logger.debug("API Key is Available..")

    logger.info(f"Setting DSPY LM: {model_name}")
    lm = dspy.LM(model_name)
    dspy.configure(lm=lm)


def generate_data(examples: List[Dict]) -> List[Dict]:
    lm_module = GenerateSuggestions()

    logger.info("Generating responses for the examples")
    data = []
    for i, example in tqdm(
        enumerate(examples), desc="Generating response", total=len(examples)
    ):
        output = lm_module(**example)
        reason, response = output.reasoning, output.response
        example["answer"] = f"{reason} {response}"

        data.append(example)

        if i == 5:
            break

    return data


def load_examples() -> Dict:

    logger.info(f"Loading the Exapmles from Path - {DATA_PATH / 'exmaples.json'}")
    with open(DATA_PATH / "examples.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    logger.info(f"Successfully loaded {len(data)} examples.")
    return data


def main(model_name: str) -> None:
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
