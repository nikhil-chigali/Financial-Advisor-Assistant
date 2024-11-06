#!/bin/bash

# Set the output log file path
LOG_FILE="logs/runs_log_exp.txt"

# Array with month names for logging purposes
MONTH_NAMES=(January February March April May June July August September October November December)

# Function to log messages
log_message() {
    echo "$1" >> "$LOG_FILE"
}

# Loop through each month from January (1) to December (12)
for month in {1..10}
do 
    start_date="2024-$(printf "%02d" $month)-01"
    end_date="2024-$(printf "%02d" $((month + 1)))-01"
    month_name="${MONTH_NAMES[$((month - 1))]}" # Get month name from array

    log_message "--------- Start date: $start_date | End date: $end_date ---------"
    
    # Download news from Alpaca
    log_message "Downloading news from Alpaca for $month_name"
    # python3 scripts/download_news_from_alpaca.py --from_date "$start_date" --to_date "$end_date"
    log_message "Downloading news from Alpaca for $month_name - finished"
    
    # Embed and push news to Qdrant
    log_message "Embedding and Pushing news to Qdrant for $month_name"
    # python3 scripts/embed_news_into_qdrant.py --from_date "$start_date" --to_date "$end_date" --num_processes 2
    log_message "Embedding and Pushing news to Qdrant for $month_name - finished"
done
