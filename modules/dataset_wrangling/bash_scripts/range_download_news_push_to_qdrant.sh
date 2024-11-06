#!/bin/bash

# Set the output log file path
LOG_FILE="logs/runs_log.txt"

# Array with month names for logging purposes
MONTH_NAMES=(January February March April May June July August September October November December)

# Function to log messages
log_message() {
    echo "$1" >> "$LOG_FILE"
}

# Get the year and start month from arguments (default to full year if not provided)
YEAR=${1:-2024}
START_MONTH=${2:-1}
END_MONTH=${3:-$((START_MONTH + 1))} # Set END_MONTH to START_MONTH + 1 if not provided

# Ensure END_MONTH does not exceed 12 (December)
if [ "$END_MONTH" -gt 12 ]; then
    END_MONTH=12
fi

# Loop through each specified month
for month in $(seq $START_MONTH $END_MONTH)
do 
    start_date="$YEAR-$(printf "%02d" $month)-01"
    end_date="$YEAR-$(printf "%02d" $((month + 1)))-01"
    month_name="${MONTH_NAMES[$((month - 1))]}" # Get month name from array

    log_message "--------- Start date: $start_date | End date: $end_date ---------"
    
    # Download news from Alpaca
    log_message "Downloading news from Alpaca for $month_name $YEAR"
    python3 scripts/download_news_from_alpaca.py --from_date "$start_date" --to_date "$end_date"
    log_message "Downloading news from Alpaca for $month_name $YEAR - finished"
    
    # Embed and push news to Qdrant
    log_message "Embedding and Pushing news to Qdrant for $month_name $YEAR"
    python3 scripts/embed_news_into_qdrant.py --from_date "$start_date" --to_date "$end_date" --num_processes 2
    log_message "Embedding and Pushing news to Qdrant for $month_name $YEAR - finished"
done
