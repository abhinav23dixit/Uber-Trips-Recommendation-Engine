from fuzzywuzzy import process
import pandas as pd

def interest_finder(interest: str, interests: pd.DataFrame):
    all_interests = interests['INTEREST*'].tolist()
    closest_match = process.extractOne(interest, all_interests)
    return closest_match[0]


def get_interest_index(interest: str, interest_mapper, interest_to_id_mapper, interests: pd.DataFrame):
    fuzzy_interest = interest_finder(interest, interests)
    interest_id = interest_to_id_mapper[fuzzy_interest]
    interest_idx = interest_mapper[interest_id]
    return interest_idx


def get_interest(interest_idx: str, interest_inv_mapper, interest_id_inv_mapper):
    interest_id = interest_inv_mapper[interest_idx]
    interest = interest_id_inv_mapper[interest_id]
    return interest


def see_user_top_interests(ratings: pd.DataFrame, interests: pd.DataFrame, user_id):
    user_ratings = ratings[ratings['USER_ID*'] == user_id].merge(interests[['INTEREST_ID*', 'INTEREST*']])
    user_ratings = user_ratings.sort_values('RATING*', ascending=False)
    print(user_ratings.head(10))


def read_dataset(path: str):
    csv_df = pd.read_csv(path)
    print(csv_df.head())
    return csv_df
