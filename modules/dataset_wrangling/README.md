# News Analysis and Training Data Generation Pipeline

A comprehensive pipeline for collecting financial news from Alpaca, processing it using NLP techniques, storing it in a vector database, and generating training data using Large Language Models.

## 🌟 Features

- **News Collection**: Automated fetching of news articles from Alpaca API
- **Text Processing**: Advanced NLP pipeline for cleaning and chunking text
- **Vector Database**: Efficient storage and retrieval using Qdrant
- **Training Data Generation**: AI-powered data generation using GPT models
- **Parallel Processing**: Support for multi-process operations
- **Structured Logging**: Comprehensive logging system for debugging

## 🏗️ Architecture

The system consists of three main components:

1. **Data Collection**

   - Fetches news from Alpaca API
   - Handles pagination and batch processing
   - Saves raw data in JSON format

2. **Processing Pipeline**

   - Cleans and structures news articles
   - Generates embeddings using sentence-transformers
   - Stores vectors in Qdrant database

3. **Training Data Generation**
   - Uses OpenAI models for data generation
   - Implements Chain of Thought reasoning
   - Generates structured training examples

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Qdrant instance (cloud or local)
- Alpaca API credentials
- OpenAI API key

### Installation

1. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

2. Install dependencies using Poetry

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate the poetry shell
poetry shell
```

3. Set up environment variables

```bash
# Create .env file with the following variables

APCA_API_KEY_ID="your-alpaca-key"
APCA_API_SECRET_KEY="your-alpaca-secret"
QDRANT_API_URL="your-qdrant-url"
QDRANT_API_KEY="your-qdrant-key"
OPENAI_API_KEY="your-openai-key"

# you can refer to the .env.example file for the same.
```

## 📋 Usage

### 1. Generate Training Data using an LLM.

```bash
python scripts/generate_training_data.py \
    --model "openai/gpt-4o"
```

### 2. Download News Data using the Alpaca API.

```bash
python scripts/download_news_from_alpaca.py \
    --from_date "2024-01-01" \
    --to_date "2024-01-31"
```

### 3. Process and Embed News into Qdrant DB.

```bash
python scripts/embed_news_into_qdrant.py \
    --from_date "2024-01-01" \
    --to_date "2024-01-31" \
    --num_processes 4
```

## 📁 Project Structure

```
modules/dataset_wrangling/
├── data/               # Data storage
│   └── raw_news/      # Raw JSON files
├── logs/              # Log files
├── scripts/           # Main execution scripts
└── src/              # Source code
    ├── alpaca_api.py         # Alpaca integration
    ├── news_documents.py     # Document processing
    ├── dspy_datagen.py      # Training data generation
    ├── vector_db_api.py     # Qdrant integration
    ├── paths.py             # Project paths
    └── utils.py             # Utility functions
```

## 🔧 Configuration

The system uses several configuration parameters:

- **Vector Size**: 384 (MiniLM-L6-v2)
- **Batch Size**: 50 articles per API call
- **Distance Metric**: Cosine similarity (Qdrant)
- **Supported LLMs**:
  - openai/gpt-4o
  - openai/gpt-4o-mini
  - openai/gpt-3.5-turbo

## 📝 Logging

The system implements comprehensive logging using `loguru`:

- Log files are stored in `logs/detailed_logs.log`
- Maximum log file size: 50 MB
- Log retention: 20 days
- Debug level logging available

## ⚠️ Important Notes

- Ensure proper API credentials are set in the `.env` file
- Monitor API rate limits for Alpaca and OpenAI
- Check disk space for vector database storage
- Consider memory requirements for parallel processing
