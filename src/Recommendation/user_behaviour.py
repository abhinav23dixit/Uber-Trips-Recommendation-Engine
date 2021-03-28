import numpy as np
import pandas as pd
from Recommendation.utils import get_interest, read_dataset, get_interest_index, interest_finder, see_user_top_interests
from constants import top_user_interests_limit, OTHERS_REGEX


def generate_complete_user_interest_dataset(ratings, interests):
    expanded_df = pd.merge(ratings, interests, how='left', on='INTEREST_ID*')
    expanded_df = expanded_df.drop(['INTEREST_ID*'], axis=1)
    return expanded_df


def get_others_flag(interest):
    return OTHERS_REGEX in interest


def get_rsorted_activities(activities: list):
    activities_dict = {}
    for activity in activities:
        if activity not in activities_dict:
            activities_dict[activity] = 1
        else:
            activities_dict[activity] += 1

    rsorted_activties = []
    rsort_orders = sorted(activities_dict.items(), key=lambda x: x[1], reverse=True)
    for activity_order in rsort_orders:
        rsorted_activties.append(activity_order[0])
    return rsorted_activties


def get_highly_rated_interests(user_id: int, rated_df: pd.DataFrame, threshold: int = top_user_interests_limit):
    user_ratings = rated_df[rated_df['USER_ID*'] == user_id]
    user_ratings = user_ratings.sort_values('RATING*', ascending=False)
    user_ratings['REDUNDANT_INTEREST_FLAG*'] = user_ratings['INTEREST*'].apply(lambda x: get_others_flag(x))
    user_ratings = user_ratings[user_ratings['REDUNDANT_INTEREST_FLAG*'] != True]
    user_ratings = user_ratings.head(threshold)
    return user_ratings['INTEREST*'].to_list()


def get_highly_rated_activities(user_id: int, rated_df: pd.DataFrame):
    user_ratings = rated_df[rated_df['USER_ID*'] == user_id]
    user_ratings['REDUNDANT_INTEREST_FLAG*'] = user_ratings['INTEREST*'].apply(lambda x: get_others_flag(x))
    user_ratings = user_ratings[user_ratings['REDUNDANT_INTEREST_FLAG*'] != True]
    user_ratings['ACTIVITY*'] = user_ratings['INTEREST*'].apply(lambda x: x[:x.rindex(" ")])
    activities = user_ratings['ACTIVITY*'].to_list()
    return get_rsorted_activities(activities)

# for independent testing
# if __name__ == '__main__':
#     ratings = read_dataset("Dataset/Rated User Interests.csv")
#     interests = read_dataset("Dataset/Interests Dataset.csv")
#     users = read_dataset("Dataset/Users Dataset.csv")
#
#     expanded_df = generate_complete_user_interest_dataset(ratings, interests)
#     filtered_df = expanded_df[expanded_df['USER_ID*'] == 3]
    # print(get_highly_rated_interests(user_id=3, rated_df=expanded_df, threshold=3))
    # print(get_highly_rated_activities(user_id=3, rated_df=expanded_df))
