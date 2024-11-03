# for month in {10..11}
# do 
#     echo "--------- Start date: 2024-$((month-1))-01 | End date: 2024-$((month))-01 ---------" >> logs/runs_log.txt
#     echo "Downloading news from Alpaca" >> logs/runs_log.txt
#     python3 scripts/download_news_from_alpaca.py --from_date "2024-$((month-1))-01" --to_date "2024-$((month))-01"
#     echo "Downloading news from Alpaca - finished" >> logs/runs_log.txt
#     echo "Embedding and Pushing news to Qdrant" >> logs/runs_log.txt
#     python3 scripts/embed_news_into_qdrant.py --from_date "2024-$((month-1))-01" --to_date "2024-$((month))-01" --num_processes 2
#     echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt
# done



# echo "--------- Start date: 2024-09-01 | End date: 2024-10-01 ---------" >> logs/runs_log.txt
# echo "Downloading news from Alpaca" >> logs/runs_log.txt
# python3 scripts/download_news_from_alpaca.py --from_date "2024-09-01" --to_date "2024-10-01"
# echo "Downloading news from Alpaca - finished" >> logs/runs_log.txt
# echo "Embedding and Pushing news to Qdrant" >> logs/runs_log.txt
# python3 scripts/embed_news_into_qdrant.py --from_date "2024-09-01" --to_date "2024-10-01" --num_processes 2
# echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt





echo "Embedding and Pushing news to Qdrant - January" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-01-01" --to_date "2024-02-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt

echo "Embedding and Pushing news to Qdrant - February" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-02-01" --to_date "2024-03-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt

echo "Embedding and Pushing news to Qdrant - March" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-03-01" --to_date "2024-04-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt

echo "Embedding and Pushing news to Qdrant - April" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-04-01" --to_date "2024-05-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt

echo "Embedding and Pushing news to Qdrant - May" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-05-01" --to_date "2024-06-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt

echo "Embedding and Pushing news to Qdrant - June" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-06-01" --to_date "2024-07-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt

echo "Embedding and Pushing news to Qdrant - July" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-07-01" --to_date "2024-08-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt

echo "Embedding and Pushing news to Qdrant - August" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-08-01" --to_date "2024-09-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt

echo "Embedding and Pushing news to Qdrant - September" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-09-01" --to_date "2024-10-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt

echo "Embedding and Pushing news to Qdrant - October" >> logs/runs_log.txt
python3 scripts/embed_news_into_qdrant.py --from_date "2024-10-01" --to_date "2024-11-01" --num_processes 2
echo "Embedding and Pushing news to Qdrant - finished" >> logs/runs_log.txt
