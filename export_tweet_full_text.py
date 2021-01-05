import os

import pandas as pd


def get_full_text(parquet_list, tweet_id):
    tweet_id = str(tweet_id)
    for parquet_file in parquet_list:
        a = parquet_file['tweet_id']
        tweet = parquet_file[parquet_file['tweet_id'] == tweet_id]
        if len(tweet) == 1:
            return tweet['full_text'].values[0]
    return None


if __name__ == '__main__':
    query_path = 'full_queries.txt'
    data_path = r'Data'
    my_csv_file_path = r'316299031.csv'

    load_query = pd.read_csv(query_path, delimiter='\n', header=None)
    query_data_frame = load_query.T.apply(lambda row: ''.join(row.loc[0].split('.')[1:]))
    parquet_list = []
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".parquet"):
                rel_dir = os.path.relpath(root, data_path)
                rel_file = os.path.join(rel_dir, file)
                parquet_list.append(pd.read_parquet(data_path + "\\" + rel_file, engine="pyarrow"))

    my_csv_file = pd.read_csv(my_csv_file_path)
    my_csv_file_new_coloumn = my_csv_file.T.apply(lambda row: get_full_text(parquet_list, row['tweet']))
    my_csv_file_query_text = my_csv_file.T.apply(lambda row: query_data_frame.loc[row['query'] - 1])
    my_csv_file['query_text'] = my_csv_file_query_text
    my_csv_file['full_text'] = my_csv_file_new_coloumn
    my_csv_file.to_csv(my_csv_file_path[:-4] + "_with_full_text.csv", index=False)
