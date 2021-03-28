import pandas as pd
import csv
def transform_time_columns(dataset_df: pd.DataFrame):
    return dataset_df


def load_dataset(path):
    return pd.read_csv(path)

if __name__ == '__main__':
    dataset_df = load_dataset('Synthetic User Trips Data.csv')
    transformed_time_col_df = transform_time_columns(dataset_df)
